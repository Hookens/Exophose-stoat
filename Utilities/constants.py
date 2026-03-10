from enum import StrEnum, IntEnum


class Env:
    API_TOKEN = ""  # PUT YOUR API TOKEN HERE
    DBHOST = ""  # PUT YOUR SERVER'S HOST HERE
    DBUSER = ""  # PUT YOUR SERVER'S USER HERE
    DBPASSWORD = ""  # PUT YOUR SERVER'S PASSWORD HERE
    DBCATALOG = ""  # POUT YOUR SERVER'S DATABASE HERE


class Limits:
    ALLOW_LIMIT = 10
    CREATE_LIMIT = 5
    BUNDLE_LIMIT = 5
    BUNDLE_ALLOW_LIMIT = 10
    BUNDLE_ROLE_LIMIT = 20


class Indicators(IntEnum):
    MAXIMUM_REACHED = 0
    ADDABLE = 1
    PRESENT = 2
    UNABLE = 3


class Identity:
    BOT = ""  # CHOOSE YOUR BOT NAME
    PREFIX = ""  # CHOOSE YOUR PREFIX

    # It would be cool if you could leave those as-is so people know who made the bot originally
    NAME = "Hookens#1427"
    ID = "01KH7D7DBAHT0TB3M06X2886DZ"
    EMOTE = ":01KHQ680C2ZYKG1HN4C3NHGAKH:"


class LoadOrder:
    GEARS = [
        "Debug.logging",
        "Utilities.events",
        "Utilities.data",
        "Utilities.embeds",
        "Commands.handling",
        "Debug.debugmethods",
        "Debug.debugcommands",
        "Utilities.utilities",
        "Utilities.verification",
        "Admin.adminmethods",
        "Admin.admincommands",
        "Help.helpmethods",
        "Help.helpcommands",
        "User.usermethods",
        "User.usercommands",
        "Bundle.bundlemethods",
        "Bundle.bundlecommands",
    ]


class LoggingDefaults:
    CHANNEL = ""  # PUT YOUR LOG CHANNEL ID HERE
    GEAR_COUNT = len(LoadOrder.GEARS)


class EmbedDefaults:
    STYLE = "#4000AF"
    SUCCESS = "#00CC00"
    FAILURE = "#CC0000"


class HelpDefaults:
    class Menus(StrEnum):
        CUSTOM_CONFIG = "CC"
        BUNDLE_CONFIG = "BC"
        CUSTOM_ROLES = "CR"
        BUNDLE_ROLES = "BR"

    PREFIX = ""  # PUT THE BOT PREFIX AGAIN HERE (It's duplicated so you can make the ping "<@ID>" the prefix and still have it displayed properly as "@Exophose" in help, for example.)
    COLOR = EmbedDefaults.STYLE

    # It would be cool if you could leave those as-is so people know where to find the bot
    BOT_INVITE = "[Have it for yourself :01KHQ68H4HNYJQRSN26A5MA4TN:](https://stoat.chat/bot/01KHMM0YME8WZYK4EJ1YV8NYYA)"
    SUPPORT_SERVER = "[For updates, feedback & issues :01KHQ688SMN559DHQGN2MG16V1:](https://stt.gg/aKFcCTdJ)"
    SUPPORT_ME = "[It's entirely optional :01KHQ67RXSYA4TAMMV4B798ZEZ:](https://ko-fi.com/hookens)"
    SOURCE_CODE = "[Host it yourself :01KHQ6CSRN9NFC271VGRD9BCAM:](https://github.com/Hookens/Exophose-stoat)"


class DebugLists:
    GEARS = [
        "AdminCommands",
        "AdminMethods",
        "BundleCommands",
        "BundleMethods",
        "DebugCommands",
        "DebugMethods",
        "Logging",
        "Handling",
        "HelpCommands",
        "HelpMethods",
        "UserCommands",
        "UserMethods",
        "Data",
        "Embeds",
        "Events",
        "Utilities",
        "Verification",
    ]


class AdminTexts:
    C_ALLOW = "Allow a role to use role management commands. Members of this role will be able to create, rename, recolor and remove their own custom role(s)."
    C_DISALLOW = "Disallow a role from using role management commands."
    C_ALLOWED = "List currently allowed roles in your server along with their relevant information."

    F_ALLOWROLE = "Role to allow. **Required**"
    F_DISALLOWROLE = "Role to disallow. **Required**"
    F_MAX = f"Maximum number of roles that a user with that role can create. Number ≤ **{Limits.CREATE_LIMIT}**"
    # F_BADGES = "Can add custom badges."
    # F_PUBLIC = "Make this message public."

    E_ALLOW = f"`{HelpDefaults.PREFIX}allow %Supporters`"
    E_DISALLOW = f"`{HelpDefaults.PREFIX}allow %Supporters`"


class BundleTexts:
    CHOICES = [
        "add",
        "remove",
    ]

    C_CREATE = "Create an empty bundle. Add roles to it using `bundle edit` and allow its usage with `bundle allow`."
    C_LIST = "List created bundles, their roles, and which roles are allowed."
    C_EDIT = "Add or remove a role in a bundle. These roles represent the color choices users will have."
    C_DELETE = "Deletes a bundle and its associations. This operation is irreversible."
    C_ALLOW = "Allow a role to use a bundle. This will let users with this role to choose colors from this bundle"
    C_DISALLOW = "Disallow a role from using a bundle."

    F_NAME = "Name of the bundle. **Required** | Length ≤ **100**"
    F_ACTION = "Edition action for the bundle. **Required** | **add** or **remove**"
    F_ROLE = "Role to add or remove. **Required**"
    F_INDEX = "Index of the bundle. Refer to the bundle list. **Required**"
    F_CONFIRM = "Confirm the name of the bundle by including it. **Required**"
    F_ALLOWROLE = AdminTexts.F_ALLOWROLE
    F_DISALLOWROLE = AdminTexts.F_DISALLOWROLE

    E_CREATE = f'`{HelpDefaults.PREFIX}bundle create "Epic colors"`'
    E_EDIT = f"`{HelpDefaults.PREFIX}bundle edit 1 %CoolPurple add`"
    E_DELETE = f'`{HelpDefaults.PREFIX}bundle delete 1 "Epic colors"`'
    E_ALLOW = f"`{HelpDefaults.PREFIX}bundle allow 1 %Supporters`"
    E_DISALLOW = f"`{HelpDefaults.PREFIX}bundle disallow 1 %Supporters`"

    C_CHOICES = "List roles that are available to you based upon the roles you currently possess."
    C_CHOOSE = "Pick a role from the choices given to you."

    F_CHOICE = "Index of the role. Refer to the choices list."

    E_CHOOSE = f"`{HelpDefaults.PREFIX}bundle choose 3`"


class DebugTexts:
    C_ANNOUNCE = "Make an announcement embed."
    C_SHUTDOWN = "Ends the bot thread."
    C_RELOAD = "Reload a gear."
    C_STATUS = "Get bot gears' status."

    F_TITLE = "Title for the announcement. **Required** | Length ≤ **100**"
    F_DESCRIPTION = "Description for the announcement. **Required** | Length ≤ **1024**"
    F_CHANNEL = "The channel in which the announcement will be posted."
    F_GEAR = "Gear that needs to be reloaded. **Required**"

    E_ANNOUNCE = f'`{HelpDefaults.PREFIX}announce "This is a title" "This is the content" #announcements`'


class HelpTexts:
    C_HELP = "Show the help menu."
    F_PUBLIC = "If you wish to make this message public."


class UserTexts:
    C_CREATE = "Assign yourself a custom role. Colors use the hexadecimal format, such as `#8C24EC`. If the color cannot be parsed, it will be considered as being raw CSS, such as `linear-gradient`, and will be passed on without verification."
    C_REMOVE = "Remove a custom role."
    C_RECOLOR = "Recolor a custom role. Colors use the hexadecimal format, such as `#8C24EC`. If the color cannot be parsed, it will be considered as being raw CSS, such as `linear-gradient`, and will be passed on without verification."
    C_RENAME = "Rename a custom role."
    # C_REBADGE = "Rebadge a custom role. Leave empty to remove it."
    C_CREATED = "List created roles."

    F_NAME = "Name for the role. **Required** | Length ≤ **32**"
    F_COLOR = "Color for your role. **Required** | Length ≤ **1000**"
    # F_BADGE = "Badge for your role."
    F_INDEX = "Index of the role."
    F_MEMBER = "Member to list the created roles for."

    E_CREATE = f'`{HelpDefaults.PREFIX}create "Stoat Enjoyer" #8C24EC`'
    E_REMOVE = f"`{HelpDefaults.PREFIX}remove`"
    E_RECOLOR = f"`{HelpDefaults.PREFIX}recolor #4000AF`"
    E_RENAME = f'`{HelpDefaults.PREFIX}rename "Exophose Enjoyer"`'
    E_CREATED = f"`{HelpDefaults.PREFIX}created @Hookens`"

    DELETE_REASON = "Impossible to connect to the SQL database at the moment."
    # DF_NO_BADGE_PERMS = "Your server does not support custom role badges."
    # DF_NOT_BADGE_ALLOWED = "You do not have badge permissions with your currently allowed role(s)."
    # DF_INVALID_FILE = "The file you have provided is invalid. Make sure it's an image file type supported by Stoat (.png, .jpg, .webp)."
