from kabaret.app.ui.gui.widgets.flow.flow_view import CustomPageWidget, QtWidgets, QtCore, QtGui
from kabaret.app import resources

from ..resources.icons import gui as _


class FileMatchItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, package_item, file):
        super(FileMatchItem, self).__init__(package_item)
        self._file = None
        self.set_file(file)

    def set_file(self, file):
        self._file = file
        self._refresh()
    
    def _refresh(self):
        f = self._file

        self.setText(0, f['file_label'])

        department = f['department']
        name = f['name']

        if not self.valid():
            icon = QtGui.QIcon(resources.get_icon(
                ('icons.gui', 'warning')
            ))
            self.setIcon(1, icon)
        else:
            self.setIcon(1, QtGui.QIcon())
            if department is None and name is None:
                self.setText(1, '-')
            else:
                target_text = '%s/%s' % (f['department'], f['name'])
                if f['relpath'] is not None:
                    target_text += '/' + f['relpath']
                
                self.setText(1, target_text)
        
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        self._paint()
    
    def update(self):
        target = self.current_target()

        if target is None: # undefined target
            self._file['undefined'] = True
            self._file['to_ignore'] = False
        else:
            self._file['undefined'] = False
            self._file['department'], self._file['name'], self._file['relpath'] = target
            self._file['to_ignore'] = (target == (None, None, None))
        
        self._refresh()
        self.parent().update()
    
    def current_target(self):
        '''
        Returns the target depending on the current
        text of the item. This is currently an
        illegal method as it checks the text itself.
        '''
        target_text = self.text(1)
        target = None

        if target_text == '-':
            target = (None, None, None)
        else:
            while target_text.startswith('/'): target_text = target_text[1:]
            while target_text.endswith('/'): target_text = target_text[:-1]
            target_fields = tuple(target_text.split('/', 2))
            target_len = len(target_fields)

            if target_len >= 2:
                target_dept = target_fields[0]
                target_name = target_fields[1]
                target_relpath = None

                if target_len >= 3:
                    target_relpath = target_fields[2]
                
                target = (target_dept, target_name, target_relpath)
        
        return target
    
    def _paint(self):
        if self.to_ignore():
            color = QtGui.QColor(80, 80, 80)
        else:
            color = QtGui.QColor(185, 194, 200)
        
        for i in range(self.treeWidget().header().count()):
            self.setForeground(i, QtGui.QBrush(color))

    def valid(self):
        return not self._file['undefined']
    
    def to_ignore(self):
        return self._file['to_ignore']
    
    def to_dict(self):
        department = name = relpath = None
        target = self.current_target()

        if target is not None:
            department, name, relpath = target
        
        f = self._file
        f.update({
            'name': name,
            'department': department,
            'relpath': relpath
        })

        return f


class PackageItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, shot_item, package):
        super(PackageItem, self).__init__(shot_item)
        self._package = None
        self.set_package(package)

    def set_package(self, package):
        self._package = package
        self._refresh()
    
    def update(self):
        self.parent().update()
    
    def _refresh(self):
        p = self._package
        self.setFlags(QtCore.Qt.ItemIsEnabled)
        self.setText(0, f'{p["department"]}/{p["name"]} {p["revision"]}')
        self.setIcon(0, QtGui.QIcon(resources.get_icon(
            ('icons.gui', 'package')
        )))

        for match in p['matches']:
            FileMatchItem(self, match)
        
        self.setExpanded(not self.valid())
    
        self._paint()
    
    def _paint(self):
        for i in range(self.treeWidget().header().count()):
            self.setBackgroundColor(i, QtGui.QColor(60, 60, 60))
    
    def valid(self):
        valid = (self.childCount() > 0)
        for i in range(self.childCount()):
            if not self.child(i).valid():
                valid = False
                break
        
        return valid
    
    def to_dict(self):
        d = self._package

        matches = []
        
        for i in range(self.childCount()):
            file_item = self.child(i)

            if not file_item.to_ignore():
                matches.append(file_item.to_dict())
        
        d.update({
            'path': self._package['path'],
            'department': self._package['department'],
            'matches': matches,
        })

        return d


class ShotItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, tree, shot):
        super(ShotItem, self).__init__(tree)
        self._shot = None
        self.set_shot(shot)

    def set_shot(self, shot):
        self._shot = shot
        self._refresh()
    
    def update(self):
        if self.valid():
            self.setIcon(1, QtGui.QIcon())
            self.setCheckState(0, QtCore.Qt.Checked)
        else:
            icon = QtGui.QIcon(resources.get_icon(
                ('icons.gui', 'warning')
            ))
            self.setIcon(1, icon)
            self.setCheckState(0, QtCore.Qt.Unchecked)
    
    def _refresh(self):
        s = self._shot
        self.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable)
        self.setCheckState(0, QtCore.Qt.Unchecked)
        self.setExpanded(True)
        self.setText(0, f'{s["sequence"]} {s["shot"]}')

        for package in s['packages']:
            PackageItem(self, package)
        
        self.update()
        self._paint()
    
    def _paint(self):
        for i in range(self.treeWidget().header().count()):
            self.setBackgroundColor(i, QtGui.QColor(70, 70, 70))
    
    def valid(self):
        valid = (self.childCount() > 0)
        for i in range(self.childCount()):
            if not self.child(i).valid():
                valid = False
                break
        
        return valid
    
    def to_dict(self):
        d = self._shot
        packages = []

        for i in range(self.childCount()):
            packages.append(self.child(i).to_dict())
        
        d.update({
            'sequence': self._shot['sequence'],
            'shot': self._shot['shot'],
            'packages': packages
        })

        return d


class PackageList(QtWidgets.QTreeWidget):

    def __init__(self, custom_widget):
        super(PackageList, self).__init__()
        self._custom_widget = custom_widget

        self.setHeaderLabels(self.get_columns())
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.refresh()

        self.itemChanged.connect(self.on_item_changed)

        self.header().resizeSections(QtWidgets.QHeaderView.ResizeToContents)

    def get_columns(self):
        return ('Source file', 'Target')
    
    def sizeHint(self):
        return QtCore.QSize(300, 500)
    
    def refresh(self):
        self.clear()

        data = self._custom_widget.get_package_files()

        for shot in data:
            ShotItem(self, shot)
    
    def on_item_changed(self, item, column):
        if column == 0 and item.checkState(0) == QtCore.Qt.Checked and not item.valid():
            item.setCheckState(0, QtCore.Qt.Unchecked)
        elif column == 1:
            item.update()


class UnpackSourcePackagesWidget(CustomPageWidget):

    def build(self):
        self.package_list = PackageList(self)
        self.button_settings = QtWidgets.QPushButton('Settings')
        self.button_refresh = QtWidgets.QPushButton(
            QtGui.QIcon(resources.get_icon(('icons.gui', 'refresh'))), ''
        )
        self.button_refresh.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button_refresh.setToolTip('Refresh list')
        self.checkbox_selectall = QtWidgets.QCheckBox('Select all')
        self.button_unpack = QtWidgets.QPushButton('Unpack')
        
        glo = QtWidgets.QGridLayout()
        glo.addWidget(self.package_list, 0, 0, 1, 5)
        glo.addWidget(self.button_settings, 1, 0)
        glo.addWidget(self.button_refresh, 1, 1)
        glo.addWidget(self.checkbox_selectall, 1, 2)
        glo.addWidget(self.button_unpack, 1, 4)
        glo.setColumnStretch(3, 10)
        glo.setSpacing(2)
        self.setLayout(glo)

        self.checkbox_selectall.stateChanged.connect(self.on_checkbox_state_changed)
        self.button_refresh.clicked.connect(self._on_refresh_button_clicked)
        self.button_settings.clicked.connect(self.on_settings_button_clicked)
        self.button_unpack.clicked.connect(self.on_unpack_button_clicked)
    
    def get_package_files(self):
        return self.session.cmds.Flow.call(
            self.oid, 'get_package_files', [], {}
        )

    def _on_refresh_button_clicked(self):
        self.package_list.refresh()
    
    def on_unpack_button_clicked(self):
        data = []
        for i in range(self.package_list.topLevelItemCount()):
            shot_item = self.package_list.topLevelItem(i)

            if shot_item.checkState(0) == QtCore.Qt.Checked:
                data.append(shot_item.to_dict())
        
        self.session.cmds.Flow.call(
            self.oid, 'unpack', [data], {}
        )
    
    def on_settings_button_clicked(self):
        pass
    
    def on_checkbox_state_changed(self, state):
        for i in range(self.package_list.topLevelItemCount()):
            item = self.package_list.topLevelItem(i)
            item.setCheckState(0, QtCore.Qt.CheckState(state))
