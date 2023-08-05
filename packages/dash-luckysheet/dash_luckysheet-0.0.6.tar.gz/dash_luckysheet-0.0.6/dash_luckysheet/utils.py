import pandas as _pd

def get_luckysheet(df: _pd.DataFrame, name="Sheet1"):
    return {
        "name": name,
        "color": "",
        "status": 1,
        "order": 0,
        "config": {
            "rowlen": {},
            "customHeight": {},
            "borderInfo": [
                {
                    "rangeType": "range",
                    "borderType": "border-all",
                    "color": "#000",
                    "style": "1",
                    "range": [
                        {
                            "row": [
                                0,
                                len(df),
                            ],
                            "column": [
                                0,
                                len(df.columns)-1
                            ],
                        }
                    ]
                },
                {
                    "rangeType": "range",
                    "borderType": "border-all",
                    "color": "#000",
                    "style": "8",
                    "range": [
                        {
                            "row": [
                                0,
                                0
                            ],
                            "column": [
                                0,
                                len(df.columns)-1
                            ],

                        }
                    ]
                }]

        },
        "filter_select": {
            "row": [
                0,
                len(df),
            ],
            "column": [
                0,
                len(df.columns)-1
            ]},
        "data": [[{
            "m": el,
            "ct": {
                "fa": "General",
                "t": "g"
            },
            "v": el,
            "bl": 1,
            "fs": "11"
        } for el in df.columns], *df.values.tolist()],
        "row": len(df)+1,
        "column": len(df.columns),
        "scrollLeft": 0,
        "scrollTop": 0,
        "frozen": {
            "type": "row"
        },

    }
