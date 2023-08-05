from tests import compatibility_issues

## PRIVATE CALDAV SERVER(S) TO RUN TESTS TOWARDS
## Make a list of your own servers/accounts that you'd like to run the
## test towards.  Running the test suite towards a personal account
## should generally be safe, it should not mess up with content there
## and it should clean up after itself, but don't sue me if anything
## goes wrong ...

## Define your primary caldav server here
caldav_servers = [
    {
        'url': "https://xandikos.tobixen.no/",
        "password": "kalenderfestøl",
        "username": "tobias",
        'incompatibilities': compatibility_issues.xandikos,
        'enable': True
    },
    {
        'url': 'https://cloud.domainedessablons.fr/remote.php/dav/',
        'password': 'VeyshleewdmynJig7ob',
        'username': 'tobixen',
        'incompatibilities': compatibility_issues.nextcloud + ['unique_calendar_ids', 'non_existing_calendar_found', 'sticky_events'], ## the two latter seems to be a sticky calendar thing and/or impossible to create two calendars with the same name
        'enable': True # not working 100% as of 2022-04 ?
    },
    {
        'url': 'https://ecloud.global/remote.php/dav/',
        'username': 'tobixen@e.email',
        'password': '/Test4Caldav.',
        'incompatibilities': compatibility_issues.nextcloud,
        'enable': True
    },
    {
        ## <gregn@fastmail.com>
        'url': 'https://caldav.luckydrawcalendar.com/dav.php',
        'username': 'alpha',
        'password': 'passwordpassword',
        'incompatibilities': compatibility_issues.baikal,
        'enable': True
    },
    {
        'url': 'https://zimbra.redpill-linpro.com/dav/',
        'username': 'tobias@redpill-linpro.com',
        'password': 'fiskesuppe kyllingsalat',
        'incompatibilities': compatibility_issues.zimbra,
        'enable': True
    },
    {
        ## Does not get a proper response on get-current-principal propfind.
        ## should do more research into it, maybe
        'url': 'http://dav.cladmi.eu/cal.php/calendars/tbrox/default/',
        'username': 'tbrox',
        'password': 'testdigestauthenticationtbrox',
        'enable': False
    },
    {
        'url': 'http://calendar.tobixen.no:80/caldav.php/',
        'username': 'tobias',
        'password': '/family.',
        'enable': True,
        'incompatibilities': compatibility_issues.davical + [ 'no_freebusy_rfc4791' ]
    },

    ## It's needed with manual intervention to refresh accounts:
    {
        'url': 'https://demo2.nextcloud.com/remote.php/dav/',
        'username': 'RQ6PbYE6KaNpfmHY',
        'password': 'demo2',
        'incompatibilities': compatibility_issues.nextcloud,
        'enable': False
    },
    {
        'url': 'https://caldav.fastmail.com/dav/',
        'username': 'pythoncaldavtest@fastmail.com',
        'password': 'Q66M664VUQVJQ4ZJ',
        'incompatibilities': compatibility_issues.fastmail,
        'enable': False
    },
    
]

if True:
    for x in caldav_servers:
        x['enable'] = False
    caldav_servers[6]['enable']=True

    test_xandikos = False
    test_radicale = False
else:
    test_xandikos = True
    test_radicale = True


#caldav_servers = caldav_servers[1:2]
rfc6638_users = []
#for user in ('alpha', 'bravo', 'delta'):
#    rfc6638_users.append({'url': 'https://caldav.luckydrawcalendar.com/dav.php', 'username': user, 'password': 'passwordpassword'})

## SOGo virtual test server
## I did roughly those steps to set up a SOGo test server:
## 1) I download the ZEG - "Zero Effort Groupware" - from https://sourceforge.net/projects/sogo-zeg/
## 2) I installed virtualbox on my laptop
## 3) "virtualbox ~/Downloads/ZEG-5.0.0.ova" (TODO: probably it's possible to launch it "headless"?)
## 4) I clicked on some buttons to get the file "imported" and started
## 5) I went to "tools" -> "preferences" -> "network" and created a NatNetwork
## 6) I think I went to ZEG -> Settings -> Network and chose "Host-only Adapter"
## 7) SOGo was then available at http://192.168.56.101/ from my laptop
## 8) I added the lines below to my conf_private.py
#caldav_servers.append({
#    'url': 'http://192.168.56.101/SOGo/dav/',
#    'username': 'sogo1'.
#    'password': 'sogo'
#})
#for i in (1, 2, 3):
#    sogo = caldav_servers[-1].copy()
#    sogo['username'] = 'sogo%i' % i
#    rfc6638_users.append(sogo)

## MASTER SWITCHES FOR TEST SERVER SETUP
## With those configuration switches, pre-configured test servers in conf.py
## can be turned on or off

## test_public_test_servers - Use the list of common public test
## servers from conf.py.  As of 2020-10 no public test servers exists, so this option
## is currently moot :-(
test_public_test_servers = False

## test_private_test_servers - test using the list configured above in this file.
test_private_test_servers = True

## For usage by ../examples/scheduling_examples.py.  Should typically
## be three different users on the same caldav server.
#rfc6638_users = [ caldav_servers[0], caldav_servers[1], caldav_servers[2] ]
