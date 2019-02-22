zlogs_definitions = {
    "timeline_timezone": 'Driver timezone',
    "report_breadcrumb": 'Driver Logs',
    "report_title": 'Driver Logs',
    "links": {
        "driver-list": "Driver List",
        "unidentified-logs": "Unidentified Driving Trips",
        "unidentified-events": "Unidentified Driving Events",
        "pending-edits": "Pending Edits",
        "edited-logs": "Edited Logs"
    },
    "pdf_export": {
        "shipping_ids": "Shipping ID(s)",
        "team_drivers": "Team Driver(s)",
        "trailer_ids": "Trailer ID(s)",
        "miles_in_24hr_period": "{unit} in 24 Hr Period",
        "cmv_power_unit": "CMV Power Unit",
        "driver_name": "Driver Name",
        "driver_id": "Driver IDs",
        "driver_license_number": "Driver License #",
        "us_dot_number": "USDOT #",
        "eld_id": "ELD ID",
        "eld_manufacturer": "ELD Manufacturer",
        "time_zone": "Time Zone",
        "period_starting_time": "24 Period Starting Time",
        "exempt_driver_status": "Exempt Driver Status",
        "carrier": "Carrier",
        "cdl": "CDL",
        "vin": "VIN",
        "english": "Miles",
        "metric": "Kilometers",
        "no_driver_logs": "No Driver Logs found for this date"
    },
    # https://github.com/ZonarSystems/pyzhos/blob/master/zhos/models/eld_event_enums.py#L50
    # https://confluence.zonarsystems.net/pages/viewpage.action?pageId=51511797
    "eld_event_origin": {
        # 1
        "SYSTEM": 'ELD',
        # 2
        "DRIVER": "Driver",
        # 3
        "NON_DRIVER": 'Carrier',
        # 4
        "UNIDENTIFIED_DRIVING": "Unidentified" # TODO waiting for final text
    },
    "eld_event_type": {
        # 1
        "DUTY_STATUS": {
            "eld_event_code": {
                # 1
                "OFF_DUTY": {
                    "header": "{origin} changed duty status to Off Duty",
                    "name": "Off Duty",
                    "abbr": "OFF"
                },
                # 2
                "SB": {
                    "header": "{origin} changed duty status to Sleeper Berth",
                    "name": "Sleeper Berth",
                    "abbr": "SB"
                },
                # 3
                "DRIVING": {
                    "header": "{origin} changed duty status to Driving",
                    "name": "Driving",
                    "abbr": "D"
                },
                # 4
                "ON_DUTY": {
                    "header": "{origin} changed duty status to On Duty",
                    "name": "On Duty",
                    "abbr": "ON"
                }
            }
        },
        # 2
        "INTERMEDIATE": {
            "eld_event_code": {
                # 1
                "INTERMEDIATE_CONVENTIONAL_LOC": {
                    "header": "Intermediate location captured",
                    "name": "Immediate location captured",
                    "abbr": ""
                },
                # 2
                "INTERMEDIATE_REDUCED_LOC": {
                    "header": "Intermediate location captured",
                    "name": "Immediate location captured",
                    "abbr": ""
                }
            }
        },
        # 3
        "SDS": {
            "name": "Duty Status",
            "eld_event_code": {
                # 1
                "PC": {
                    "header": "{origin} indicated Authorized Personal Use of CMV started",
                    "name": "Authorized Personal Use of CMV",
                    "abbr": "PC"
                },
                # 2
                "YM": {
                    "header": "{origin} indicated Yard Move started",
                    "name": "Yard Move",
                    "abbr": "YM"
                },
                # 100
                "WT": {
                    "header": "{origin} indicated Oil Well Wait Time started",
                    "name": "Oil Well Wait Time",
                    "abbr": "WT"
                },
                # 101
                "HR": {
                    "header": "{origin} indicated Yard Move (Hi Rail) started",
                    "name": "Yard Move (Hi Rail)",
                    "abbr": "HR"
                },
                # 200
                "CLEAR_PC": {
                    "header": "{origin} indicated Authorized Personal Use of CMV cleared",
                    "name": "Authorized Personal Use of CMV",
                    "abbr": "PC"
                },
                # 201
                "CLEAR_YM": {
                    "header": "{origin} indicated Yard Move cleared",
                    "name": "Yard Move",
                    "abbr": "YM"
                },
                # 202
                "CLEAR_WT": {
                    "header": "{origin}  indicated Oil Well Wait Time cleared",
                    "name": "Oil Well Wait Time",
                    "abbr": "WT"
                },
                # 203
                "CLEAR_HR": {
                    "header": "{origin}  indicated Yard Move (Hi Rail) cleared",
                    "name": "Yard Move (Hi Rail)",
                    "abbr": "HR"
                }
            }
        },
        # 4
        "CERTIFICATION": {
            "name": "Certification",
            "header": "{origin} certified daily log: :log_date ",
        },
        # 5
        "AUTH_STATUS": {
            "name": "Auth Status",
            "eld_event_code": {
                # 1
                "LOGIN": {
                    "header": "{origin} logged into ELD",
                    "name": "",
                    "abbr": ""
                },
                # 2
                "LOGOUT": {
                    "header": "{origin} logged out of ELD",
                    "name": "",
                    "abbr": ""
                }
            }
        },
        # 6
        "ENGINE_STATUS": {
            "name": "Engine Status",
            "eld_event_code": {
                # 1
                "POWER_UP_CONVENTIONAL_LOC": {
                    "header": "Engine power-up",
                    "name": "Engine power-up",
                    "abbr": ""
                },
                # 2
                "POWER_UP_REDUCED_LOC": {
                    "header": "Engine power-up",
                    "name": "Engine power-up",
                    "abbr": ""
                },
                # 3
                "POWER_DOWN_CONVENTIONAL_LOC": {
                    "header": "Engine shut-down",
                    "name": "Engine shut-down",
                    "abbr": ""
                },
                # 4
                "POWER_DOWN_REDUCED_LOC": {
                    "header": "Engine shut-down",
                    "name": "Engine shut-down",
                    "abbr": ""
                }
            }
        },
        # 7
        "DIAG_MAL": {
            "name": "Diagnostic Malfunction",
            "eld_event_code": {
                # 1
                'MALFUNCTION_SET': {
                    "header": "ELD {malfunction_type} created",
                    "name": "Malfunction created",
                    "short_name": "Created",
                    "abbr": ""
                },
                # 2
                'MALFUNCTION_CLEAR': {
                    "header": "ELD {malfunction_type} cleared",
                    "name": "Malfunction cleared",
                    "short_name": "Cleared",
                    "abbr": ""
                },
                # 3
                'DIAGNOSTIC_SET': {
                    "header": "ELD {diagnostic_type} created",
                    "name": "Diagnostic created",
                    "short_name": "Created",
                    "abbr": ""
                },
                # 4
                'DIAGNOSTIC_CLEAR': {
                    "header": "ELD {diagnostic_type} cleared",
                    "name": "Diagnostic cleared",
                    "short_name": "Cleared",
                    "abbr": ""
                }
            },
            "eld_diagnostic_code": {
                # 1
                "POWER": {
                    "name": "Power Data Diagnostic Event"
                },
                # 2
                "ENGINE_SYNCH": {
                    "name": "Engine Synchronization Data Diagnostic Event"
                },
                # 3
                "MISSING_REQUIRED_DATA": {
                    "name": "Missing Required Data Elements Data Diagnostic Event"
                },
                # 4
                "DATA_TRANSFER": {
                    "name": "Data Transfer Data Diagnostic Event"
                },
                # 5
                "UNIDENTIFIED_DRIVING": {
                    "name": "Unidentified Driving Records Data Diagnostic Event"
                },
                # 6
                "OTHER": {
                    "name": "Other ELD Identified Diagnostic Event"
                }
            },
            "eld_malfunction_code": {
                # P
                "POWER": {
                    "name": "Power Compliance Malfunction"
                },
                # E
                "ENGINE_SYNCH": {
                    "name": "Engine Synchronization Compliance Malfunction"
                },
                # L
                "POSITIONING": {
                    "name": "Positioning Compliance Malfunction"
                },
                # R
                "DATA_RECORDING": {
                    "name": "Data Recording Compliance Malfunction"
                },
                # S
                "DATA_TRANSFER": {
                    "name": "Data Transfer Compliance Malfunction"
                },
                # O
                "OTHER": {
                    "name": "Other ELD Detected Malfunction"
                }
            }
        },
        # 100
        "SYSTEM_DESCRIPTOR": {
            "name": "System Descriptor",
            "eld_event_code": {
                # 1
                'OUTSIDE_RADIUS': {
                    "header": "{origin} System Descriptor changed to {code}",
                    "name": "",
                    "abbr": ""},
                # 2
                'UNDOCKED': {
                    "header": "{origin} System Descriptor changed to {code}",
                    "name": "",
                    "abbr": ""},
                # 3
                'GPS_LOCK': {
                    "header": "ELD captured location from GPS",
                    "name": "",
                    "abbr": ""},
                # 4
                'AUTO_INSERT': {
                    'header': 'Midnight log captured',
                    'name': 'Midnight Log',
                    'abbr': ''
                }
            }
        },
        # 101
        "APPLIED_USER_DESCRIPTOR": {
            "name": "Applied User Descriptor",
            "eld_event_code": {
                # 1
                'BIGDAY': {
                    "header": "{origin} Applied {code} exemption",
                    "name": "Big Day",
                    "abbr": ""
                },
                #2
                'ADVERSE_WEATHER': {
                    "header": "{origin} Applied {code} exemption",
                    "name": "Adverse Weather",
                    "abbr": ""
                },
                #3
                'RESTART': {
                    "header": "{origin} Applied {code} exemption",
                    "name": "34 hour restart",
                    "abbr": ""
                },

                'SHORT_HAUL_14_HOUR':{
                    "header": "{origin} Applied {code} exemption",
                    "name": "Short haul 14",
                    "abbr": ""
                },
                'ON_DUTY_REST_BREAK':{
                    "header": "{origin} Applied {code} exemption",
                    "name": "On duty rest break",
                    "abbr": ""
                }
        }
    },
        # 102
        "RULESET_CHANGE": {
            "name": "Ruleset Change",
            "eld_event_code": {
                # 1
                'US_PROPERTY_60': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Property 60",
                    "abbr": ""
                },
                # 2
                'US_PROPERTY_70': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Property 70",
                    "abbr": ""
                },
                # 3
                'US_PASSENGER_60': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Passenger 60",
                    "abbr": ""
                },
                # 4
                'US_PASSENGER_70': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Passenger 70",
                    "abbr": ""
                },
                # 5
                'US_PROPERTY_70_OIL_WELL': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Oilwell 70",
                    "abbr": ""
                },
                # 6
                'US_PROPERTY_70_OIL_FIELD': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Oilfield 70",
                    "abbr": ""
                },
                # 7
                'US_PROPERTY_60_BIGDAY': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "16 Hour Exempt 60",
                    "abbr": ""
                },
                # 8
                'US_PROPERTY_70_BIGDAY': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "16 Hour Exempt 70",
                    "abbr": ""
                },
                # 9
                'CA_SOUTH60_CYCLE1': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "CA South 60 Cycle 1",
                    "abbr": ""
                },
                # 10
                'CA_SOUTH60_CYCLE2': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "CA South 60 Cycle 2",
                    "abbr": ""
                },
                # 11
                'US_PROPERTY_60_SHORTHAUL': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Property Short Haul 60",
                    "abbr": ""
                },
                # 12
                'US_PROPERTY_70_SHORTHAUL': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Property Short Haul 70",
                    "abbr": ""
                },
                # 13
                'US_UNIVERSAL_7': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Universal 7 Day",
                    "abbr": ""
                },
                # 14
                'US_UNIVERSAL_8': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Universal 8 Day",
                    "abbr": ""
                },
                # 15 "
                'US_PROPERTY_60_CONSTRUCTION': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Construction 60",
                    "abbr": ""
                },
                # 16
                'US_PROPERTY_70_CONSTRUCTION': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Construction 70",
                    "abbr": ""
                },
                #100
                'US_PROPERTY_70_TX_OIL_WELL': {
                    "header": "{origin} ruleset changed to {code}",
                    "name": "Texas oil",
                    "abbr": ""
                }
            },
        },
        # 103
        "METADATA": {
            "name": "Metadata",
            "eld_event_code": {
                # 1
                'TRAILER_START': {
                    "header": "{origin} added trailer ",
                    "name": "",
                    "abbr": ""},
                # 2
                'TRAILER_END': {
                    "header": "{origin} removed trailer ",
                    "name": "",
                    "abbr": ""
                },
                # 3
                'DOLLY_START': {
                    "header": "{origin} added Dolly ",
                    "name": "",
                    "abbr": ""
                },
                # 4
                'DOLLY_END': {
                    "header": "{origin} removed Dolly",
                    "name": "",
                    "abbr": ""
                },
                # 5
                'LOAD_START': {
                    "header": "{origin} added load ",
                    "name": "",
                    "abbr": ""
                },
                # 6
                'LOAD_END': {
                    "header": "{origin} added load ",
                    "name": "",
                    "abbr": ""
                },
                # 7
                'CO_DRIVER_START': {
                    "header": "Co-Driver {co_driver_name} logged in",
                    "name": "",
                    "abbr": ""
                },
                # 8
                'CO_DRIVER_END': {
                    "header": "Co-Driver {co_driver_name} logged out",
                    "name": "",
                    "abbr": ""
                }
            }
        },
        # 104
        "ASSET_CHANGE": {
            "name": "Asset change",
            "eld_event_code": {
                # 1
                'ASSET_CHANGE': {
                    "header": "{origin} updated power unit number",
                    "name": "",
                    "abbr": ""}
            }
        },
        # 200
        "EFFECT_USER_DESCRIPTOR": {
            "name": "Effect User Descriptor",
            "eld_event_code": {
                # 1
                'EFFECT_BIGDAY': {
                    "header": "{origin} Effect User Descriptor changed to {code}",
                    "name": "",
                    "abbr": ""
                },
                #2
                'EFFECT_ADVERSE_WEATHER': {
                    "header": "{origin} Effect User Descriptor changed to {code}",
                    "name": "",
                    "abbr": ""
                },
                #3
                'EFFECT_RESTART': {
                    "header": "{origin} Effect User Descriptor changed to {code}",
                    "name": "",
                    "abbr": ""
                }
            }
        },
    },
    "hos_grid": {
        "legend": {
            "ok": "Okay",
            "in_violation": "In Violation",
            "sds": "Special Duty Status"
        },
        'x_axis': {
            '0': 'M',
            '12': 'N',
            '24': 'M'
        },
        'tooltip': {
            'duty_status': 'Duty Status',
            'duration': 'Duration',
            'start_time': 'Start time',
            'start_location': 'Start location'
        }
    },
    "detail_tabs": {
        "driver": "DRIVER DETAILS",
        "vehicle": "VEHICLE SETUP"
    },
    "trip_detail_tabs": {
        "trip": "TRIP DETAILS",
        "history": "HISTORY"
    },
    "event_detail_tabs": {
        "header": "EVENT DETAILS",
    },
    # TODO refactor these to use lowercase_key instead of UPPERCASE_KEY
    "driver_details": {
        "DRIVER_ID": "Driver Id",
        "EXSID": "EXSID",
        "EXEMPTION_APPLIED": "Exemption Applied",
        "ACTIVE_RULESET": "Active Ruleset",
        "CURRENT_TEAM_DRIVER": "Current Team Driver",
        "TEAM_DRIVERS": "Team Drivers",
        "TOTAL_DISTANCE": "Total Distance",
        "TOTAL_PC_DISTANCE": "Total PC Distance"
    },
    "trip_details": {
        "CURRENT_STATUS": "Current status",
        "CURRENTLY_ASSIGNED_TO": "Currently assigned to",
        "START_GPS_LOCATION": "Start GPS location",
        "START_DATE": "Start date",
        "END_GPS_LOCATION": "End GPS location",
        "END_DATE": "End date",
        "TOTAL_DISTANCE": "Total distance",
        "DURATION": "Duration",
        "LAST_KNOWN_DRIVER": "Last known driver",
        "LAST_ACTION": "Last Action"
    },
    "event_details": {
        "CURRENT_STATUS": "Current status",
        "CURRENTLY_ASSIGNED_TO": "Currently assigned to",
        "LOCATION": "Location",
        "DATE": "Date",
        "TOTAL_VEHICLE_MILES": "Total Vehicle :units",
        "TOTAL_VEHICLE_HOURS": "Total Vehicle hours"
    },
    "vehicle_details": {
        "CMV_POWER_UNIT": "CMV Power Unit",
        "VIN": "VIN",
        "CARRIER": "Carrier",
        "DOT_NUMBER": "DOT #",
        "SHIPPING_DOC": "Shipping Doc",
        "SHIPPER_COMMODITY": "Shipper/Commodity",
        "TRAILER": "Trailer",
        "DOLLY": "Dolly"
    },
    "duty_status_events": {
        "location": "Location",
        "notes": "Notes",
        "total_vehicle_miles": "Total Vehicle Miles",
        "accumulated_vehicle_miles": "Accumulated Vehicle Miles",
        "elapsed_engine_hours": "Elapsed Engine Hours",
        "total_engine_hours": "Total Engine Hours",
        "peding_edit_hover": "Edits pending driver verification",
    },
    "none_text": "none",
    "driver_log_assign_card": {
        "assign_card_header": "Assign unidentified driving trip",
        "assign_to": "Assign to",
        "driver": "Driver",
        "no_driver_reason": "No Driver Reason",
        "notes": "Notes",
        "send_to_driver": "Send to Driver",
        "assign_to_no_driver_reason": "Assign to No Driver Reason",
        "select_reason": "Select Reason",
        "update_successful_message": "Unidentified driving trip successfully assigned to|Unidentified driving trips successfully assigned to",
        "update_failed_message": "Failed to assign unidentified driving trip to|Failed to assign unidentified driving trips to",
    },
    # documentation for event codes: https://confluence.zonarsystems.net/display/MOBENG/Enums#Enums-ZonarEvents
    "driver_exemption": {
        # use key from zapy here
        "2": {
            "short": "Adverse"
        },
        "1": {
            "short": "Big day"
        },
        "5": {
            "short": "SHaul 14"
        }
    },
    "driver_event_card": {
        "system_notes": "Exemption Applied to Drive time at :time"
    },
    # https://confluence.zonarsystems.net/display/UX/HOS+Clocks
    "ruleset_clocks": {
        1: { # Property 60
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '60 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        2: { # Property 70
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '70 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        3: { # Passenger 60
            1: { 'label': '10 HR' },
            2: { 'label': '15 HR' },
            5: { 'label': '60 HR' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        4: { # Passenger 70
            1: { 'label': '10 HR' },
            2: { 'label': '15 HR' },
            5: { 'label': '70 HR' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        5: {# Oilwell 60
        },
        6: { # Oilfield 70
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '70 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        7: { # 16 hour exempt 60
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '60 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        8: { # 16 hour exempt 70
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '70 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        9: { # CA South 60 Cycle 2
            6: { 'label': '13 HR WS' },
            7: { 'label': '14 HR WS' },
            8: { 'label': '16 HR WS' },
            5: { 'label': 'Cycle 1' },
            1: { 'label': '13 HR Daily' },
            2: { 'label': '14 HR Daily' },
        },
        10: { # CA South 60 Cycle 1
            6: { 'label': '13 HR WS' },
            7: { 'label': '14 HR WS' },
            8: { 'label': '16 HR WS' },
            12: { 'label': 'Cycle 2' },
            1: { 'label': '13 HR Daily' },
            2: { 'label': '14 HR Daily' },
        },
        11: { # Property Short Haul 60
            1: { 'label': '11 HR' },
            2: { 'label': '12 HR' },
            5: { 'label': '60 HR' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        12: { # Property Short Haul 70
            1: { 'label': '11 HR' },
            2: { 'label': '12 HR' },
            5: { 'label': '70 HR' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        13: { # Universal 7 Day
            1: { 'label': 'Daily Drive' },
            5: { 'label': '7 Day' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        14: { # Universal 8 Day
            1: { 'label': 'Daily Drive' },
            5: { 'label': '8 Day' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        15: { # Construction 60
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '60 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' }
        },
        16: { # Construction 70
            1: { 'label': '11 HR' },
            2: { 'label': '14 HR' },
            5: { 'label': '70 HR' },
            3: { 'label': 'Rest Break' },
            4: { 'label': 'Off Duty' },
            10: { 'label': 'Hours Gained' },
        },
        100: { #  texas oil well 70
            1: { 'label': '12 HR' },
            2: { 'label': '15 HR' },
            5: { 'label': '70 HR' },
            4: { 'label': 'Off Duty' },
        },
    },
    "edit_driver_event": {
        "decertified_logs_message": "Pending driver certification for this day",
        "certified_logs_message": "Driver has certified this day's logs",
        "form_header": "Edit driver log",
        "start_time": "Start time",
        "total_vehicle_miles": "Total vehicle miles",
        "notes": "Notes (Minimum of 4 characters)",
        "duty_status": "Duty status",
        "location": "Location",
        "submit_return_codes": {
            "SUCCESS": "Driver event successfully updated",
            "NO_REC": "Cannot find record to edit",
            "NOT_CERTIFIED": "Day is not certified.",
            "HAS_PENDING": "Update to this event is in pending state.",
            "UNKNOWN_ERROR": "Unknown error occurred.",
            "UNKNOWN": "Unexpected exception.",
            "INVALID_EDIT_FIELD": "Cannot edit the field being edited.",
            "INVALID_EVENT_TYPE": "Cannot edit this event type, only duty status and sds.",
            "ARGS": "Missing required args.",
        }
    },
    "udl_selected_trips": {
        "trip_selected": "trip selected|trips selected",
        "clear_all_selected": "Clear all selected",
    },
    "udl_bulk_assign_info": {
    "manage_trips": "Bulk Manage Trips",
    "manage_trips_description": "Select trips from the list on the left and assign several at once to the driver",
    "exit_bulk_edit": "Exit Bulk Edit",
    },
    "filters": {
        "dispatcher_locations": "Dispatcher Locations",
        "dispatchers": "Dispatchers",
        "all_locations": "All Locations",
        "all_statuses": "All Duty Statuses",
        "all_dispatchers": "All Dispatchers",
        "status": 'Status',
        "duty_status": 'Duty Status',
        "all_event_type": 'All Event Types',
        "event_type": 'Event Type',
        "log_status": 'Status',
        "no_driver_reason": "No Driver Reason"
    },
    "export_options": {
        "pdf": "PDF Export",
        "csv": "CSV Export",
        "fmcsa": "FMCSA Output",
        "driver_log": "Export Driver Logs",
    },
    "ude_status": {
        "assigned": 'Assigned',
        'unassigned': 'Unassigned'
    },
    "driver_events": {
        "diagnostics_cleared": "Diagnostics cleared",
        "engine_power_up": "Engine power up",
        "engine_shutdown": "Engine shutdown",
        "malfunction_cleared": "Malfunction cleared",
        "bulk_info": {
            "manage_events": "Bulk Manage Events",
            "manage_events_description": "Select events from the list on the left and assign several at once to a No Driver Reason",
            "exit_bulk_edit": "Exit Bulk Manage",
        },
        "ude_selected_events": {
            "event_selected": "event selected|events selected",
            "clear_all_selected": "Clear all selected",
        },
        "ude_assign_card": {
            "form_title": "Assign unidentified driver event",
            "button_title": "Assign"
        },
        "update_successful_message": "Unidentified driving event successfully assigned to|Unidentified driving events successfully assigned to",
        "update_failed_message": "Failed to assign unidentified driving event to|Failed to assign unidentified driving events to",
    },
    "no_driver_reason_select": {
        "title": "No Driver Reason"
    },
    "distance_units_display_text": {
        "english": "miles",
        "metric": "kilometers"
    },
    "export_report_options": {
        "email": "Email",
        "web_services": "Web Services"
    },
    "export_report_update_codes": {
        "SUCCESS": "Request successfully submitted.",
        "UNKNOWN_ERROR": "Unexpected exception.",
        "ARGS": "Missing required args.",
    },
}