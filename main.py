import config
from typing import Optional
import mysql.connector
from fastapi import FastAPI, HTTPException, Header

responses = {
    404: {"description": config.strings["not_registered"]},
    403: {"description": config.strings["invalid_key"]}
}

app = FastAPI(title=config.strings["project_title"],
    description=config.strings["project_description"],
    version=config.strings["project_version"],)


def init_db():
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )


def get_cursor(dict=False):
    try:
        mydb.ping(reconnect=True, attempts=3, delay=5)
    except mysql.connector.Error as err:
        return None
    return mydb.cursor(dictionary=dict, buffered=True)


@app.get("/player/{player_name}", responses={**responses})
def read_all_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_all_stats(player_name, api_key)}


@app.get("/player/skywars/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [1, 2, 3, 6], api_key)}


@app.get("/player/uhc/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [26, 4], api_key)}


@app.get("/player/speeduhc/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [30, 31], api_key)}


@app.get("/player/pit/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [9], api_key)}


@app.get("/player/paintball/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [18], api_key)}


@app.get("/player/murdermystery/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [10, 25], api_key)}


@app.get("/player/megawalls/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [16, 17], api_key)}


@app.get("/player/duels/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [13, 14], api_key)}


@app.get("/player/blitz/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [15, 29], api_key)}


@app.get("/player/bedwars/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [7, 8, 27, 28], api_key)}


@app.get("/player/skyblock/{player_name}", responses={**responses})
def read_gamemode_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [33, 34, 35, 36, 37, 38, 39, 40], api_key)}


@app.get("/player/general/{player_name}", responses={**responses})
def read_general_stats(player_name: str, api_key: Optional[str] = Header(None)):
    return {"stats": grab_certain_stats(player_name, [19, 20, 21, 22, 23, 24, 32], api_key)}


def check_apikey(api_key):
    if api_key == config.apikey:
        return True
    return False


def grab_player_id(player_name):
    # If player id is not in cache, cache it
    if not player_name in player_id_mapping:
        mycursor = get_cursor(dict=True)
        mycursor.execute("SELECT id FROM users WHERE displayname = %s", (player_name,))
        userresult = mycursor.fetchone()
        if userresult is None:
            return None
        player_id_mapping[player_name] = userresult["id"]
    return player_id_mapping[player_name]


def readable_print_stats(stats):
    newstats = {}
    for stat in stats:
        # We already know that lb_field, just want to add a new type to the dict
        if not lb_field_mapping[stat["lb_field_id"]] in newstats:
            newstats[lb_field_mapping[stat["lb_field_id"]]] = []
        newstats[lb_field_mapping[stat["lb_field_id"]]].append({stat["type"].lower(): stat["value"]})
    return newstats


def grab_all_stats(player_name, api_key):
    if not check_apikey(api_key):
        raise HTTPException(status_code=403, detail=config.strings["invalid_key"])
    mycursor = get_cursor(dict=True)
    mycursor.execute("SELECT lb_field_id, type, value FROM lb_stats WHERE user_id = %s", (grab_player_id(player_name),))
    stats = mycursor.fetchall()
    readable_stats = readable_print_stats(stats)
    if readable_stats is None or not readable_stats:
        raise HTTPException(status_code=404, detail=config.strings["not_registered"])
    return readable_stats


def grab_certain_stats(player_name, stats_wanted, api_key):
    if not check_apikey(api_key):
        raise HTTPException(status_code=403, detail=config.strings["invalid_key"])
    mycursor = get_cursor(dict=True)
    detailquery = ""
    first = True
    for stat_wanted in stats_wanted:
        if first:
            first = False
            detailquery += "lb_field_id = " + str(stat_wanted)
        else:
            detailquery += " OR lb_field_id = " + str(stat_wanted)
    mycursor.execute("SELECT lb_field_id, type, value FROM lb_stats WHERE user_id = %s AND (" + detailquery + ")",
                     (grab_player_id(player_name),))
    stats = mycursor.fetchall()
    readable_stats =  readable_print_stats(stats)
    if readable_stats is None or not readable_stats:
        raise HTTPException(status_code=404, detail=config.strings["not_registered"])
    return readable_stats


def update_field_mapping():
    mycursor = get_cursor(dict=True)
    mycursor.execute("SELECT * FROM lb_fields")
    myresponse = mycursor.fetchall()
    for lbfield in myresponse:
        lb_field_mapping[lbfield["id"]] = lbfield["name"]


mydb = init_db()
lb_field_mapping = {}
player_id_mapping = {}

# When server starts we are grabbing the lb_fields to map friendly names on API responses
update_field_mapping()
