import os, json, xbmc, xbmcplugin, xbmcgui, xbmcaddon

ADD_OPTION = '[I][B]Add Host[/B][/I]'
DELETE_OPTION = '[I][B]Delete Host[/B][/I]'
NULL_OPTION = '[I][B]Unset XFF[/B][/I]'


def getAddonFolder():
    try:
        return xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))
    except:
        return os.getcwd()

def getSettingsFile():
    return os.path.join(getAddonFolder(), 'settings.json')


def writeSetingsFile(settings):
    json_filename = getSettingsFile()
    json_folder = os.path.dirname(json_filename)
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)
    fp = open(json_filename, 'w')
    json.dump(settings, fp)
    fp.close()


def loadSettings():
    try:
        json_filename = getSettingsFile()
        json_folder = os.path.dirname(json_filename)
        fp = open(json_filename, 'r')
        settings = json.load(fp)
        fp.close()
    except:
        settings = {}
    return settings

def addOption():
    name = xbmcgui.Dialog().input('Enter Name', type=xbmcgui.INPUT_ALPHANUM)
    if name == '':
        sys.exit(0)
    elif name.lower() == ADD_OPTION.lower():
        xbmcgui.Dialog().ok('Error', 'Invalid name')
        sys.exit(0)
    value = xbmcgui.Dialog().input('Enter IP', type=xbmcgui.INPUT_IPADDRESS)
    if value == '':
        sys.exit(0)
    
    settings[name] = value
    writeSetingsFile(settings)


def deleteOption(settings):
    names = settings.keys()
    result = xbmcgui.Dialog().select('Choose an XFF Option', names)
    if result < 0:
        sys.exit(0)
    name = names[result]
    addr = settings[name]
    new_settings = {key: value for key, value in settings.items()
                    if key is not name}
    writeSetingsFile(new_settings)
    xbmcgui.Dialog().notification('Setting updated',
                                  'Deleted XFF Option {0} ({1})'.format(name, addr),
                                  xbmcgui.NOTIFICATION_INFO)
    sys.exit(0)


my_settings = xbmcaddon.Addon(id=xbmcaddon.Addon().getAddonInfo('id'))

settings = loadSettings()

values = settings.keys()
values.insert(0, DELETE_OPTION)
values.insert(0, ADD_OPTION)
values.insert(0, NULL_OPTION)

result = xbmcgui.Dialog().select('Choose an XFF Option', values)
if result < 0:
    sys.exit(0)

if values[result] == ADD_OPTION:
    addOption()
elif values[result] == DELETE_OPTION:
    deleteOption(settings)
else:
    
    name = values[result]
    if name == NULL_OPTION:
        addr = None
    else:
        addr = settings[name]
    xbmcaddon.Addon('plugin.video.mlslive').setSetting('xff', addr)
    xbmcgui.Dialog().notification('Setting updated',
                                  'XFF set to {0} ({1})'.format(name, addr),
                                  xbmcgui.NOTIFICATION_INFO)
