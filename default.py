import os, json, xbmc, xbmcgui, xbmcaddon, xbmcvfs
from shutil import copyfile


dlg = xbmcgui.Dialog()


def log(message):
    xbmc.log('[script.advcfg] {}'.format(message), xbmc.LOGNOTICE)


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

def updateSettings():
    res = dlg.browse(1, 'Select Options JSON', 'files')
    if not res:
        return
    log('Copying {} to local settings'.format(res))
    xbmcvfs.copy(res, getSettingsFile())


def updateAddonSettings(addon_name, settings):
    addon = xbmcaddon.Addon(addon_name)
    for setting in settings:
        log('Updating "{0}" to "{1}"'.format(setting['setting'], setting['value']))
        addon.setSetting(setting['setting'], setting['value'])


def selectAddonSettings(addon_name, addon_settings):
    settings = addon_settings['settings']
    names = []
    for setting in settings:
        names.append(setting['name'])
    idx = dlg.select('Choose setting profile', names)
    log('Updating {} with "{}" configuration...'.format(addon_name, names[idx]))
    return updateAddonSettings(addon_name, settings[idx]['config'])


def selectAddon(settings):
    addons = []
    for setting in settings:
        addons.append(setting['addon'])

    if len(addons) == 0:
        dlg.ok('Error', 'Settings appear empty. Import some settings')
        sys.exit(0)

    idx = dlg.select('Choose an addon', addons)
    if idx < 0:
        sys.exit(0)

    return selectAddonSettings(addons[idx], settings[idx])


result = dlg.select('Options', ['Change Options', 'Load Config File'])
if result < 0:
    sys.exit(0)

if result == 1:
    updateSettings()
    sys.exit(0)

my_settings = xbmcaddon.Addon(id=xbmcaddon.Addon().getAddonInfo('id'))

settings = loadSettings()

selectAddon(settings)
