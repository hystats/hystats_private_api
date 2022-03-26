host = ""
user = ""
password = ""
database = ""
apikey = ""
strings = {"not_registered": "Player not registered on HyStats", "invalid_key": "Invalid API key",
           "lb_not_found": "Specified leaderboard cannot found",
           "project_title": "HyStats Private API",
           "project_description": "This API is intended only for private use within HyStats projects and requires a "
                                  "valid API key.",
           "project_version": "1.2.0"}
detailed_modes = {
    "skywars":
        {
            "ranked": [64, 71, 78, 85],
            "solo_normal": [65, 72, 79, 86],
            "solo_insane": [66, 73, 80, 87],
            "team_normal": [67, 74, 81, 88],
            "team_insane": [68, 75, 82, 89],
            "mega_normal": [69, 76, 83, 90],
            "mega_doubles": [70, 77, 84, 91]
        },
    "duels":
        {
            "classic": [123, 124, 122, 121],
            "uhc_1v1": [127, 128, 126, 125],
            "uhc_2v2": [131, 132, 130, 129],
            "uhc_4v4": [135, 136, 134, 133],
            "sw_1v1": [143, 144, 142, 141],
            "sw_2v2": [147, 148, 146, 145],
            "sumo": [139, 140, 138, 137]
        },
    "bedwars":
        {
            "solo": [44, 48, 52, 56],
            "doubles": [45, 49, 53, 57],
            "3v3v3v3": [46, 50, 54, 58],
            "4v4v4v4": [47, 51, 55, 59],
            "4v4": [62, 63, 60, 61]
        }
}
