import os
import shutil
import fileseq
import re
from fnmatch import fnmatch
from collections import defaultdict
from kabaret import flow


class UnpackTargetFile(flow.Object):

    path_template = flow.Param()
    package_department = flow.Param()
    package_name = flow.Param()
    file_department = flow.Param() # None means unset
    file_name = flow.Param() # None means unset
    file_relpath = flow.Param() # Used by folder targets only
    to_ignore = flow.BoolParam(False)


class AddTargetFile(flow.Action):

    ICON = ('icons.gui', 'plus-sign-in-a-black-circle')

    path_template = flow.SessionParam('')
    package_department = flow.SessionParam('')
    package_name = flow.SessionParam('')
    file_department = flow.SessionParam('')
    file_name = flow.SessionParam('')
    to_ignore = flow.SessionParam(False).ui(editor='bool')

    _map = flow.Parent()

    def get_buttons(self):
        return ['Add', 'Cancel']
    
    def allow_context(self, context):
        return context and context.endswith('.inline')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_target_file(
            self.path_template.get(),
            self.package_department.get(),
            self.package_name.get(),
            self.file_department.get() or None,
            self.file_name.get() or None,
            self.to_ignore.get(),
        )


class UnpackTargetFiles(flow.Map):

    add_action = flow.Child(AddTargetFile).ui(label='Add target file')

    @classmethod
    def mapped_type(cls):
        return UnpackTargetFile
    
    def columns(self):
        return ['Package', 'Template', 'Target']
    
    def add_target_file(self, path_template, pkg_department, pkg_name, file_department, file_name, to_ignore=False):
        f = self.add(f'f{len(self):04}')
        f.path_template.set(path_template)
        f.package_department.set(pkg_department)
        f.package_name.set(pkg_name)
        f.file_department.set(file_department)
        f.file_name.set(file_name)
        f.to_ignore.set(to_ignore)

        self.touch()
    
    def to_dict(self):
        '''
        {
            (pkg_name, pkg_dept): [
                {
                    path_template,
                    file_name,
                    department,
                }
            ]
        }
        '''
        d = defaultdict(list)
        for item in self.mapped_items():
            key = (item.package_name.get(), item.package_department.get())
            d[key].append({
                'path_template': item.path_template.get(),
                'file_name': item.file_name.get() or None,
                'department': item.file_department.get() or None,
                'relpath': item.file_relpath.get(),
                'to_ignore': item.to_ignore.get(),
            })
        
        return dict(d)
    
    def _fill_row_cells(self, row, item):
        row['Package'] = f'{item.package_department.get()}/{item.package_name.get()}'
        row['Template'] = item.path_template.get()

        if item.to_ignore.get():
            row['Target'] = 'ignored'
        else:
            row['Target'] = f'{item.file_department.get()}/{item.file_name.get()}'


class SafeDict(dict):
    '''
    From https://stackoverflow.com/a/17215533
    '''
    def __missing__(self, key):
        return '{' + key + '}'


class UnpackSourcePackagesAction(flow.Action):

    target_files = flow.Child(UnpackTargetFiles)
    kitsu_shot_filter   = flow.DictParam({})

    target_kitsu_status = flow.DictParam({})
    target_sg_status    = flow.DictParam({})

    _film = flow.Parent()

    def get_package_infos(self):
        '''
        (name, department)
        '''
        return self.target_files.to_dict()

    def get_package_files(self):
        '''
        {
            sequence,
            shot,
            packages: [
                {
                    name,
                    department,
                    revision,
                    path,
                    matches: [
                        {
                            name,
                            department,
                            source_file_path,
                            to_ignore,
                        }
                    ],
                    target_files: [
                        {
                            name,
                            department,
                        }
                    ]
                }
            ]
        }
        '''
        kitsu_api = self.root().project().kitsu_api()
        data = []
        package_infos = self.get_package_infos()
        
        for sequence_name, shot_name in sorted(kitsu_api.get_shots(self.kitsu_shot_filter.get())):
            shot_data = {'sequence': sequence_name, 'shot': shot_name}
            packages_data = []

            for (package_name, package_dept), target_files in package_infos.items():
                package = self.get_package_revision(sequence_name, shot_name, package_dept, package_name)

                if package is not None:
                    package_path = package.get_path()
                    package_data = {
                        'name': package_name,
                        'department': package_dept,
                        'revision': package.name(),
                        'path': package_path,
                    }
                    files_data = []

                    for file_label, file_sequence in self.list_package_files(package_path):
                        file_data = dict.fromkeys(['name', 'department', 'relpath'])
                        file_data['undefined'] = True
                        file_data['to_ignore'] = False

                        for target_file in target_files:
                            if self.match(file_label, target_file['path_template'], sequence=sequence_name, shot=shot_name):
                                relpath = target_file['relpath']

                                if not target_file['to_ignore'] and '.' not in target_file['file_name']:
                                    if relpath is None:
                                        relpath = file_label # Set file label as default relative path if undefined in preset
                                    else:
                                        relpath = os.path.join(relpath, os.path.basename(file_label)).replace('\\', '/')
                                    
                                    relpath = self._conform_file_sequence_relpath(relpath, len(file_sequence))
                                
                                file_data.update({
                                    'name': target_file['file_name'],
                                    'department': target_file['department'],
                                    'relpath': relpath,
                                    'undefined': False,
                                    'to_ignore': target_file['to_ignore'],
                                })
                                break
                        
                        file_data['file_sequence'] = file_sequence
                        file_data['file_label'] = file_label
                        files_data.append(file_data)
                
                    package_data['matches'] = files_data
                    package_data['target_files'] = target_files # Add list of available target files
                    packages_data.append(package_data)
                else:
                    # Package not created
                    self.root().session().log_warning('')
            
            shot_data['packages'] = packages_data
            data.append(shot_data)
        
        # print(data)
        return data
    
    def _conform_file_sequence_relpath(self, relpath, length):
        if length > 1 and re.match(r'.*\.\d+-\d+(#+|@+)\..*', relpath) is None:
            dirpath = os.path.dirname(relpath)
            dirname = os.path.basename(dirpath)
            ext = os.path.splitext(relpath)[1]
            relpath = f'{dirpath}/{dirname}.{1:04}-{length:04}#{ext}'
        
        return relpath
    
    def unpack(self, files_data):
        target_kitsu_status = self.target_kitsu_status.get()
        target_sg_status = self.target_sg_status.get()
        
        for data in files_data:
            sequence_name = data['sequence']
            shot_name = data['shot']
            animatic_path = None

            for package_data in data['packages']:
                print(f'Unpacking :: Unpack package {sequence_name}/{shot_name}/{package_data["department"]}/{package_data["name"]}/{package_data["revision"]}')
                matches = defaultdict(list)

                for match in package_data['matches']:
                    match_key = (match['department'], match['name'])
                    matches[match_key].append((match['file_sequence'], match['file_label'], match['relpath']))
                
                for (department, target_name), file_sequences in matches.items():
                    if '.' not in target_name: # Target is a folder
                        dst_path = self.unpack_into_folder(package_data['path'], file_sequences, sequence_name, shot_name, department, target_name)
                    else:
                        # Unpack the first file of the first sequence
                        src_path = file_sequences[0][0][0]
                        dst_path = self.unpack_into_file(package_data['path'], src_path, sequence_name, shot_name, department, target_name)
                        
                        if target_name == 'animatic.mp4': # TODO: store animatic name in package data ?
                            animatic_path = dst_path
                
                self.save_json(sequence_name, shot_name, package_data['department'], [])
            
            if target_sg_status:
                self.update_shotgrid_status(sequence_name, shot_name, target_sg_status['task'], target_sg_status['status'])
            if target_kitsu_status:
                self.update_kitsu_status(sequence_name, shot_name, target_kitsu_status['task'], target_kitsu_status['status'], animatic_path)
    
    def get_package_revision(self, sequence_name, shot_name, dept_name, package_name):
        r = None
        film_oid = self._film.oid()
        try:
            package_folder = self.root().get_object(
                f'{film_oid}/sequences/{sequence_name}/shots/{shot_name}/departments/{dept_name}/files/{package_name}'
            )
        except:
            pass
        else:
            r = package_folder.get_head_revision()
        
        return r
    
    def list_package_files(self, package_path):
        def path_in_package(package_path, file_path):
            relpath = os.path.relpath(file_path, package_path)
            return relpath.replace('\\', '/')
        
        def get_paths(root):
            paths = []
            file_sequences = fileseq.findSequencesOnDisk(root)

            for file_sequence in file_sequences:
                file_count = len(file_sequence)

                if file_count > 0:
                    if file_count > 1:
                        file_label = path_in_package(
                            package_path,
                            os.path.join(file_sequence.dirname(), file_sequence.format())
                        )
                    else:
                        file_label = path_in_package(package_path, file_sequence.index(0))
                    
                    paths.append((
                        file_label,
                        [path_in_package(package_path, f) for f in file_sequence]
                    ))
            
            return paths
        
        paths = get_paths(package_path)

        for root, dirs, _ in os.walk(package_path):
            for d in dirs:
                paths.extend(
                    get_paths(os.path.join(root, d))
                )
        
        return paths

    def match(self, path, template, **keywords):
        '''
        ...

        Do not evaluate formatting keywords in `template`
        not provided in `keywords`.
        '''
        template = template.format_map(SafeDict(keywords))
        return fnmatch(path, template)
    
    def unpack_into_file(self, package_path, source_file_path, sequence_name, shot_name, dept_name, file_name):
        film_oid = self._film.oid()
        revision_path = None

        try:
            file_map = self.root().get_object(
                f'{film_oid}/sequences/{sequence_name}/shots/{shot_name}/departments/{dept_name}/files'
            )
        except:
            pass
        else:
            name, ext = file_name.rsplit('.', 1)

            if file_map.has_file(name, ext):
                f = file_map[f'{name}_{ext}']
            else:
                f = file_map.add_file(name, ext, tracked=True)
            
            revision_path, revision_name = self._create_revision(f)
            print('Unpacking :: \t', source_file_path, f'-> {dept_name}/{file_name}/{revision_name}/{os.path.basename(revision_path)}')
            shutil.copy2(os.path.join(package_path, source_file_path), revision_path)
        
        return revision_path
    
    def unpack_into_folder(self, package_path, file_sequences, sequence_name, shot_name, dept_name, folder_name):
        film_oid = self._film.oid()
        revision_path = None

        try:
            file_map = self.root().get_object(
                f'{film_oid}/sequences/{sequence_name}/shots/{shot_name}/departments/{dept_name}/files'
            )
        except:
            pass
        else:
            if file_map.has_folder(folder_name):
                f = file_map[folder_name]
            else:
                f = file_map.add_folder(folder_name, tracked=True)
            
            revision_path, revision_name = self._create_revision(f)

            for file_paths, file_label, relpath in file_sequences:
                print('Unpacking :: \t', file_label, f'-> {dept_name}/{folder_name}/{revision_name}/{relpath}')
                sequence_dir = os.path.join(revision_path, os.path.dirname(relpath))

                if not os.path.exists(sequence_dir):
                    os.makedirs(sequence_dir)
                
                updated_paths = self.update_sequence_paths(file_paths, relpath)
                
                for i in range(len(file_paths)):
                    shutil.copy2(
                        os.path.join(package_path, file_paths[i]),
                        os.path.join(revision_path, updated_paths[i])
                    )

    def update_sequence_paths(self, file_sequence, relpath):
        if len(file_sequence) <= 1:
            return [relpath]
        
        s = fileseq.FileSequence(relpath)
        updated_paths = [
            s.frame(i) for i in range(1, len(file_sequence) + 1)
        ]

        return updated_paths
    
    def save_json(self, sequence_name, shot_name, department, files_data):
        pass

    def update_kitsu_status(self, sequence_name, shot_name, task_name, task_status, animatic_path=None):
        kitsu_api = self.root().project().kitsu_api()

        if animatic_path is not None:
            kitsu_api.upload_shot_preview(sequence_name, shot_name, task_name, task_status, animatic_path)
        else:
            kitsu_api.set_shot_task_status(sequence_name, shot_name, task_name, task_status)

    def update_shotgrid_status(self, sequence_name, shot_name, step_name, status):
        shot = self.root().get_object(f'{self._film.oid()}/sequences/{sequence_name}/shots/{shot_name}')
        sg_config = self.root().project().get_shotgrid_config()
        sg_config.set_shot_task_status(shot.shotgrid_id.get(), step_name, status)

    def _create_revision(self, f):
        r = f.add_revision()
        revision_path = r.get_path()
        f.last_revision_oid.set(r.oid())
        os.makedirs(os.path.dirname(revision_path), exist_ok=True)

        return revision_path, r.name()

    def _fill_ui(self, ui):
        ui['custom_page'] = 'libreflow.pianoplayer.ui.unpacking.UnpackSourcePackagesWidget'
