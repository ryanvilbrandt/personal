from time import localtime, gmtime, strftime
from fpdf import FPDF

from pypdf_definitions import zlogs_definitions

FONT = "Helvetica"

HEADER_TEXT_FONT_SIZE = 15
PAGE_MARGIN_TOP = 15
PAGE_MARGIN_SIDES = 10
HEADER_LINE_HEIGHT = 8
EVENT_HEADER_LINE_HEIGHT = 5
LINE_HEIGHT = 4
PAGE_WIDTH = 190
PAGE_HEIGHT = 270

HEADER_LOGO_HEIGHT = 16
HEADER_LOGO_WIDTH = 50
HEADER_LOGO_PATH = "inputs/zonar-black.png"

ZC_ROYAL = (0x00, 0x74, 0xCD)
ZC_GHOST = (0xE2, 0xE4, 0xE6)
ZC_BLACK = (0x29, 0x32, 0x39)
ZC_SLATE = (0xA2, 0xAA, 0xAF)
ZC_GREY = (0x5B, 0x67, 0x70)
ZC_LIGHT_TICK = (0xC0, 0xC0, 0xC0)
ZC_OK = (0x4A, 0xCF, 0x49)
ZC_VIOLATION = (0xEE, 0x4C, 0x38)
ZC_SDS = (0x5B, 0x67, 0x70)

EVENT_DESCRIPTION_HEADER_FONT_SIZE = 12
NORMAL_FONT_SIZE = 10
LABEL_FONT_SIZE = 9
TIME_FORMAT = '%H:%M:%S'
SECONDS_IN_A_DAY = 86400
EVENT_DESCRIPTION_MIN_LINE_NUM = 2
EVENT_DESCRIPTION_MIN_LINE_NUM_BUBBLE = 3

GRID_AREA_HEIGHT = 54
GRID_WIDTH = 144
GRID_HEIGHT = 48
GRID_X = 10 + PAGE_MARGIN_SIDES
GRID_Y = 0
GRID_LINE_OVERLAP = 3.5
MAJOR_TICK_LENGTH = 4
MINOR_TICK_LENGTH = 2
DAY_NUMBER_X_OFFSET = -1.5
DAY_NUMBER_Y_OFFSET = 3
GRID_FONT_SIZE = 12
GRID_DUTY_STATUS_LABEL_X_OFFSET = -5
GRID_DUTY_STATUS_LABEL_Y_OFFSET = 6
GRID_DUTY_STATUS_CLOCK_X_OFFSET = 5
GRID_DUTY_STATUS_CLOCK_Y_OFFSET = 6
GRID_DUTY_STATUS_BAR_TOP_OFFSET = 2
GRID_DUTY_STATUS_BAR_HEIGHT = 8

DUTY_STATUSES = {"OFF_DUTY": 1, "SB": 2, "DRIVING": 3, 'ON_DUTY': 4}

METERS_IN_A_MILE = 1609.34

LOG_EVENT_HEIGHT = 20
LOG_EVENT_CIRCLE_RADIUS = 8
LOG_EVENT_CIRCLE_X_OFFSET = 1
LOG_EVENT_CIRCLE_Y_OFFSET = 0
LOG_EVENT_ABBR_X_OFFSET = 8.5
LOG_EVENT_ABBR_Y_OFFSET = 8.5
LOG_EVENT_TIME_X_OFFSET = 0
LOG_EVENT_TIME_Y_OFFSET = 20
LOG_EVENT_TIME_Y_OFFSET_CENTERED = 10
LOG_EVENT_TEXT_X_OFFSET = 20
LOG_EVENT_TEXT_Y_OFFSET = 2

EVENTS_FOR_TOTAL_MILES_PRECISE = [
    'CERTIFICATION',
    'AUTH_STATUS',  # Log in/Log out
    'DIAG_MAL',  # Diagnosis, Malfunction
]

EVENTS_FOR_ACCUMULATED_MILES = [
    'DUTY_STATUS',
    'SDS',  # covers both start and clear
    'INTERMEDIATE',
]

EVENTS_FOR_TOTAL_MILES = [
    'CERTIFICATION',
    'AUTH_STATUS',  # Log in/Log out
    'DIAG_MAL',  # Diagnosis, Malfunction
    'ENGINE_STATUS',  # Key on, Key off
]

EVENTS_WITHOUT_LOCATION = [
    'ASSET_CHANGE',
    'CERTIFICATION',
    'APPLIED_USER_DESCRIPTOR',
    'METADATA',
    'RULESET_CHANGE'
]


def horizontal_line(pdf, line_height=LINE_HEIGHT, line_width=PAGE_WIDTH):
    pdf.set_draw_color(*ZC_SLATE)
    pdf.ln(line_height)
    x, y = pdf.get_x(), pdf.get_y()
    pdf.line(x, y, x + line_width, y)
    pdf.ln(line_height)


def header(pdf):
    # Set fonts
    pdf.set_text_color(*ZC_GREY)
    pdf.set_font(FONT, '', HEADER_TEXT_FONT_SIZE)

    # Add image
    pdf.image(HEADER_LOGO_PATH, PAGE_MARGIN_SIDES, PAGE_MARGIN_TOP - HEADER_LOGO_HEIGHT / 4, HEADER_LOGO_WIDTH)
    pdf.cell(HEADER_LOGO_WIDTH)

    # Add header text
    pdf.cell(100, HEADER_LINE_HEIGHT, txt='Driver Logs')

    # Add date
    pdf.cell(0, HEADER_LINE_HEIGHT, txt="02/19/2019", align='R')

    # New line
    pdf.ln(HEADER_LINE_HEIGHT)

    # Add line
    horizontal_line(pdf, HEADER_LINE_HEIGHT)


def add_driver_data(data, columns):
    column_width = PAGE_WIDTH / columns
    while data:
        # Handle each row of columns individually
        workspace = data[:columns]
        data = data[columns:]

        # Write labels
        pdf.set_font_size(LABEL_FONT_SIZE)
        pdf.set_text_color(*ZC_GHOST)
        for label, text in workspace:
            pdf.cell(column_width, txt=label)
        pdf.ln(LINE_HEIGHT)

        # Write text items
        pdf.set_font_size(NORMAL_FONT_SIZE)
        pdf.set_text_color(*ZC_GREY)
        for label, text in workspace:
            pdf.cell(column_width, txt=text)
        pdf.ln(LINE_HEIGHT)
        pdf.ln(LINE_HEIGHT)


def draw_ticks(y_offset, number_of_ticks, tick_separation, tick_offset, tick_length):
    """
    Draws both major and minor ticks in the ZLogs grid. Draws equally spaced ticks.
    :param y_offset: Starting point of the bottom of the tick
    :param number_of_ticks: Number of ticks to draw
    :param tick_separation: How far apart each tick is
    :param tick_offset: x offset of starting tick, to the right
    :param tick_length: How far the tick extends upwards
    """
    for i in range(number_of_ticks):
        x = GRID_X + i * tick_separation + tick_offset
        pdf.line(x, y_offset, x, y_offset - tick_length)


def draw_base_grid(pdf, start_x, start_y, bar_height, day_width):
    # Draw shading
    pdf.set_fill_color(*ZC_SLATE)
    pdf.set_fill_color(*ZC_GHOST)
    pdf.rect(GRID_X, start_y + GRID_Y + bar_height, GRID_WIDTH, bar_height, 'DF')
    pdf.rect(GRID_X, start_y + GRID_Y + bar_height * 3, GRID_WIDTH, bar_height, 'DF')

    # Draw grid lines
    pdf.set_draw_color(*ZC_SLATE)
    y = start_y + GRID_Y
    for i in range(25):
        x = GRID_X + i * day_width
        pdf.line(x, y, x, y + GRID_HEIGHT + GRID_LINE_OVERLAP)


def draw_grid_decorations(pdf, start_x, start_y, bar_height, day_width):
    # Draw major ticks
    major_tick_offset = day_width / 2
    # Draw light colored major ticks
    pdf.set_draw_color(*ZC_LIGHT_TICK)
    draw_ticks(start_y + GRID_Y + bar_height * 1, 24, day_width, major_tick_offset, MAJOR_TICK_LENGTH)
    draw_ticks(start_y + GRID_Y + bar_height * 3, 24, day_width, major_tick_offset, MAJOR_TICK_LENGTH)
    # Draw dark colored major ticks
    pdf.set_draw_color(*ZC_SLATE)
    draw_ticks(start_y + GRID_Y + bar_height * 2, 24, day_width, major_tick_offset, MAJOR_TICK_LENGTH)
    draw_ticks(start_y + GRID_Y + bar_height * 4, 24, day_width, major_tick_offset, MAJOR_TICK_LENGTH)

    # Draw minor ticks
    minor_tick_separation = day_width / 2
    minor_tick_offset = day_width / 4.0
    # Draw light colored minor ticks
    pdf.set_draw_color(*ZC_LIGHT_TICK)
    draw_ticks(start_y + GRID_Y + bar_height * 1, 48, minor_tick_separation, minor_tick_offset, MINOR_TICK_LENGTH)
    draw_ticks(start_y + GRID_Y + bar_height * 3, 48, minor_tick_separation, minor_tick_offset, MINOR_TICK_LENGTH)
    # Draw dark colored minor ticks
    pdf.set_draw_color(*ZC_SLATE)
    draw_ticks(start_y + GRID_Y + bar_height * 2, 48, minor_tick_separation, minor_tick_offset, MINOR_TICK_LENGTH)
    draw_ticks(start_y + GRID_Y + bar_height * 4, 48, minor_tick_separation, minor_tick_offset, MINOR_TICK_LENGTH)

    # Draw grid border
    pdf.set_draw_color(*ZC_BLACK)
    pdf.rect(GRID_X, start_y + GRID_Y, GRID_WIDTH, GRID_HEIGHT)

    # Draw day numbers
    pdf.set_text_color(*ZC_GREY)
    pdf.set_font_size(NORMAL_FONT_SIZE)
    y = start_y + GRID_HEIGHT + DAY_NUMBER_Y_OFFSET
    pdf.set_xy(GRID_X, y)
    for i in range(25):
        pdf.set_xy(i * day_width + GRID_X + DAY_NUMBER_X_OFFSET, y)
        pdf.rotate(30)
        pdf.cell(2, txt=str(i), align='R')
    pdf.rotate(0)

    # Draw Duty Status Labels
    pdf.set_font_size(GRID_FONT_SIZE)
    x = GRID_X + GRID_DUTY_STATUS_LABEL_X_OFFSET
    y = start_y + GRID_Y + GRID_DUTY_STATUS_LABEL_Y_OFFSET
    pdf.set_xy(x, y)
    pdf.cell(4, txt="OFF", align='R')
    y += bar_height
    pdf.set_xy(x, y)
    pdf.cell(4, txt="SB", align='R')
    y += bar_height
    pdf.set_xy(x, y)
    pdf.cell(4, txt="D", align='R')
    y += bar_height
    pdf.set_xy(x, y)
    pdf.cell(4, txt="ON", align='R')


def draw_grid(pdf, re_summary):
    start_x, start_y = pdf.get_x(), pdf.get_y()
    bar_height = GRID_HEIGHT / 4
    day_width = GRID_WIDTH / 24
    draw_base_grid(pdf, start_x, start_y, bar_height, day_width)

    # Parse clock values
    duty_status_totals = re_summary["duty_status_totals"]
    clocks = ["", "", "", ""]
    total_seconds = 0
    for d in duty_status_totals:
        total_seconds += d['seconds']
        clocks[d['event_code'] - 1] = strftime(TIME_FORMAT, gmtime(d['seconds']))
    total_clock = strftime(TIME_FORMAT, gmtime(total_seconds))
    # Draw duty status clocks
    pdf.set_font_size(GRID_FONT_SIZE)
    x = GRID_X + GRID_WIDTH + GRID_DUTY_STATUS_CLOCK_X_OFFSET
    y = start_y + GRID_Y + GRID_DUTY_STATUS_LABEL_Y_OFFSET
    for clock in clocks:
        pdf.set_xy(x, y)
        pdf.cell(10, txt=clock)
        y += bar_height
    pdf.set_xy(x, start_y + GRID_Y + GRID_HEIGHT + DAY_NUMBER_Y_OFFSET)
    pdf.cell(10, txt=total_clock)

    # Draw grid lines
    def get_bar_x_position(epoch, re_summary):
        """
        Takes an epoch value, and returns its x position on the PDF based on the start_epoch, end_epoch,
        and width and location of the grid view.
        :param epoch:
        :param re_summary:
        :return:
        """
        relative_x_position = max(0, (epoch - re_summary['start_epoch']) / float(SECONDS_IN_A_DAY))
        return relative_x_position * GRID_WIDTH + GRID_X

    duty_statuses = re_summary["duty_statuses"]
    for duty_status in duty_statuses:
        if duty_status['violations']:
            color = ZC_VIOLATION
        elif duty_status['sds']:
            color = ZC_SDS
        else:
            color = ZC_OK
        start = get_bar_x_position(duty_status['start_epoch'], re_summary)
        end = get_bar_x_position(duty_status['end_epoch'], re_summary)
        width = end - start
        y = start_y + GRID_Y + bar_height * (DUTY_STATUSES[duty_status['event_code_name']] - 1) + \
            GRID_DUTY_STATUS_BAR_TOP_OFFSET
        pdf.set_fill_color(*color)
        pdf.rect(start, y, width, GRID_DUTY_STATUS_BAR_HEIGHT, style='DF')

    draw_grid_decorations(pdf, start_x, start_y, bar_height, day_width)

    # Set cursor to below the grid, on a new line
    pdf.set_xy(start_x, start_y + GRID_AREA_HEIGHT)
    horizontal_line(pdf)


def get_event_header(event, event_type, event_code):
    origin = zlogs_definitions["eld_event_origin"].get(event.get("event_record_origin_name"))
    co_driver_name = (event.get("data", {}).get("co_driver_first_name", "") + " " +
                      event.get("data", {}).get("co_driver_last_name", ""))
    co_driver_name = co_driver_name.strip()
    diagnostic_type = event_type.get("eld_diagnostic_code", {}).get(event.get("dcode_name"), {}).get("name")
    malfunction_type = event_type.get("eld_malfunction_code", {}).get(event.get("mcode_name"), {}).get("name")
    header = event_code.get("header") or event_type.get("header", "")
    return header.format(
        origin=origin,
        code=event_code.get("name", ""),
        co_driver_name=co_driver_name,
        diagnostic_type=diagnostic_type,
        malfunction_type=malfunction_type
    )


def draw_log_event(pdf, event):
    start_x, start_y = pdf.get_x(), pdf.get_y()

    event_type = zlogs_definitions.get("eld_event_type", {}).get(event["event_type_name"])
    event_code = event_type.get("eld_event_code", {}).get(event["event_code_name"])

    pdf.set_text_color(*ZC_BLACK)

    # Draw Duty Status circle and event time
    if event_code and event_code.get("abbr"):
        # Draw circle
        pdf.set_draw_color(*ZC_ROYAL)
        pdf.set_fill_color(*ZC_GHOST)
        diameter = LOG_EVENT_CIRCLE_RADIUS * 2
        pdf.ellipse(start_x + LOG_EVENT_CIRCLE_X_OFFSET, start_y + LOG_EVENT_CIRCLE_Y_OFFSET,
                    diameter, diameter, style="DF")
        # Draw duty status abbreviation
        pdf.set_xy(start_x + LOG_EVENT_ABBR_X_OFFSET, start_y + LOG_EVENT_ABBR_Y_OFFSET)
        pdf.cell(1, txt=event_code.get("abbr"), align='C')
        # Set cursor to event time location
        pdf.set_xy(start_x + LOG_EVENT_TIME_X_OFFSET, start_y + LOG_EVENT_TIME_Y_OFFSET)
    else:
        pdf.set_xy(start_x + LOG_EVENT_TIME_X_OFFSET, start_y + LOG_EVENT_TIME_Y_OFFSET_CENTERED)
    pdf.set_font_size(EVENT_DESCRIPTION_HEADER_FONT_SIZE)
    pdf.cell(0, txt=strftime(TIME_FORMAT, localtime(event["epoch"])))

    # Draw log event header
    pdf.set_xy(start_x + LOG_EVENT_TEXT_X_OFFSET, start_y)
    pdf.cell(0, EVENT_HEADER_LINE_HEIGHT, txt=get_event_header(event, event_type, event_code))
    pdf.ln(EVENT_HEADER_LINE_HEIGHT)
    pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)

    # Draw location
    pdf.set_font_size(NORMAL_FONT_SIZE)
    if event["event_type_name"] not in EVENTS_WITHOUT_LOCATION:
        pdf.cell(0, LINE_HEIGHT, txt="Location: " + (event.get("location") or "N/A"))
        pdf.ln(LINE_HEIGHT)
        pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)

    def get_accum_odo(event):
        if not event.get("accum_odo"):
            return "Not Available"
        return str(int(round(event.get("accum_odo") / METERS_IN_A_MILE)))

    def get_accum_hrs(event):
        if not event.get("accum_hrs"):
            return "Not Available"
        return round(event.get("accum_hrs"), 1)

    def get_odo(event):
        if event.get("is_manual_odo"):
            return str(event.get("odo"))
        if not event.get("odo"):
            return "Not Available"
        return str(round(event.get("odo") / METERS_IN_A_MILE))

    # Draw accumulated miles/hours
    if event["event_type_name"] in EVENTS_FOR_ACCUMULATED_MILES and not event.get("reduced_precision"):
        # Accum miles/hours
        text = "Accumulated Vehicle Miles: {}    Elapsed Engine Hours: {}".format(
            get_accum_odo(event),
            get_accum_hrs(event)
        )
        pdf.cell(0, LINE_HEIGHT, txt=text)
        pdf.ln(LINE_HEIGHT)
        pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)
        # Total vehicle miles
        pdf.cell(0, LINE_HEIGHT, txt="Total Vehicle Miles: " + get_odo(event))
        pdf.ln(LINE_HEIGHT)
        pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)

    # Draw total vehicle miles/hours
    if ((event["event_type_name"] in EVENTS_FOR_TOTAL_MILES_PRECISE and not event.get("reduced_precision")) or
        event["event_type_name"] in EVENTS_FOR_TOTAL_MILES):
        text = "Total Vehicle Miles: {}    Total Engine Hours: {}".format(
            get_odo(event),
            round(event.get("accum_hrs"), 1) if event.get("accum_hrs") else "Not Available"
        )
        pdf.cell(0, LINE_HEIGHT, txt=text)
        pdf.ln(LINE_HEIGHT)
        pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)

    if event.get("comments"):
        pdf.multi_cell(
            PAGE_WIDTH - PAGE_MARGIN_SIDES * 2 - LOG_EVENT_TEXT_X_OFFSET,
            LINE_HEIGHT,
            txt="Notes: " + event.get("comments")
        )
        pdf.ln(LINE_HEIGHT)
        pdf.set_x(start_x + LOG_EVENT_TEXT_X_OFFSET)

    # Set cursor to below the event, on a new line
    pdf.set_xy(start_x, max(pdf.get_y() - LINE_HEIGHT, start_y + LOG_EVENT_HEIGHT))
    horizontal_line(pdf)


def draw_log_events(pdf, event_list):
    if not event_list:
        pdf.cell(0, "No Driver data for this date")
        return

    for event in event_list:
        if pdf.get_y() - PAGE_MARGIN_TOP + LOG_EVENT_HEIGHT + LINE_HEIGHT * 2 > PAGE_HEIGHT:
            pdf.add_page()
            header(pdf)
        draw_log_event(pdf, event)


if __name__ == "__main__":
    pdf = FPDF()
    pdf.set_margins(PAGE_MARGIN_SIDES, PAGE_MARGIN_TOP)

    # Page 1
    pdf.add_page()
    header(pdf)
    # Add Driver Data
    data = [
        ("Driver Name", "Driver3 Justin"),
        ("Driver IDs", "62"),
        ("Driver License #", "C74D97B01EAEE"),
        ("USDOT #", "47"),
        ("ELD ID", "ZONAR1"),
        ("ELD Manufacturer", "Zonar Systems"),
        ("Time Zone", "PST8PDT"),
        ("24 Period Starting Time", "00:00:00"),
        ("Exempt Driver Status", ""),
        ("Carrier", "dbr47_rep1023")
    ]
    add_driver_data(data, 4)

    # Page 2
    pdf.add_page()
    header(pdf)
    pdf.cell(0, txt="01/21/2019", align='R')
    horizontal_line(pdf, line_height=HEADER_LINE_HEIGHT)
    data = [("Team Driver(s)", "")]
    add_driver_data(data, 1)
    horizontal_line(pdf)
    data = [
        ("Shipping ID(s)", ""),
        ("Trailer ID(s)", ""),
        ("Miles in 24 Hr Period", "0 Miles"),
        ("CMV Power Unit", ""),
    ]
    add_driver_data(data, 3)
    horizontal_line(pdf)

    re_summary = {
      'clocks': [
        {
          'active': True,
          'allotted': 252000,
          'clock': 5,
          'duration': 138579,
          'violation_code': '8D',
          'violation_state': 'OK'
        },
        {
          'active': True,
          'allotted': 39600,
          'clock': 1,
          'duration': 0,
          'violation_code': 'DD',
          'violation_state': 'V'
        },
        {
          'active': True,
          'allotted': 50400,
          'clock': 2,
          'duration': 0,
          'violation_code': 'DOD',
          'violation_state': 'V'
        },
        {
          'active': True,
          'allotted': 28800,
          'clock': 3,
          'duration': 0,
          'violation_code': 'DR',
          'violation_state': 'V'
        },
        {
          'active': False,
          'allotted': 0,
          'clock': 4,
          'duration': 0
        },
        {
          'active': False,
          'allotted': 0,
          'clock': 10,
          'duration': 0
        },
        {
          'active': False,
          'allotted': 0,
          'clock': 100,
          'duration': 0
        }
      ],
      'distance_driven': 0,
      'distance_pc': 0,
      'duty_status_totals': [
        {
          'event_code': 3,
          'seconds': 86399
        },
        {
          'event_code': 4,
          'seconds': 0
        },
        {
          'event_code': 2,
          'seconds': 0
        },
        {
          'event_code': 1,
          'seconds': 0
        }
      ],
      'duty_statuses': [
        {
          'end_epoch': 1550651378,
          'event_code_name': 'DRIVING',
          'event_type_name': 'DUTY_STATUS',
          'sds': None,
          'start_epoch': 1550622578,
          'violations': None
        },
        {
          'end_epoch': 1550735999,
          'event_code_name': 'DRIVING',
          'event_type_name': 'DUTY_STATUS',
          'sds': None,
          'start_epoch': 1550651378,
          'violations': [
            {
              'code': 'DD',
              'ruleset_id': 2
            },
            {
              'code': 'DOD',
              'ruleset_id': 2
            },
            {
              'code': 'DR',
              'ruleset_id': 2
            }
          ]
        }
      ],
      'end_epoch': 1550735999,
      'ruleset': 2,
      'start_epoch': 1550649600,
      'violation_state': 'V'
    }

    draw_grid(pdf, re_summary)

    event_list = [
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:29:49',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622589,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '5b9b9a79-3e24-43ad-b0ad-80056e732540',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:49',
          'location': None,
          'odo': 0,
          'oid': '5b9b9a79-3e24-43ad-b0ad-80056e732540',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:29:40',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550622580,
          'event_code_id': 2,
          'event_code_name': 'LOGOUT',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': 'a6cf4a6f-09e7-4114-8bdd-d903fdd9e04c',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:40',
          'location': None,
          'odo': 0,
          'oid': 'a6cf4a6f-09e7-4114-8bdd-d903fdd9e04c',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': '',
          'data': {
            'user_notes': ''
          },
          'driver_ts': '2019-02-19 16:29:38',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550622578,
          'event_code_id': 3,
          'event_code_name': 'DRIVING',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_record_status_id': 1,
          'event_record_status_name': 'ACTIVE',
          'event_type_id': 1,
          'event_type_name': 'DUTY_STATUS',
          'has_pending_edits': False,
          'id': '68c045d2-264a-43c2-a7ea-c78cf549fa42',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:38',
          'location': None,
          'odo': 0,
          'oid': '68c045d2-264a-43c2-a7ea-c78cf549fa42',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'DG/MAL created from UDL',
          'data': {
            'condition': 'DG/MAL created from UDL',
            'dcode': 3,
            'debug_info': '{"trip_state_id": 4, "end_geolocation": {"nearest_city": "Seattle", "nearest_lon": -122.3320708, "nearest_distance": 911.1300968188009, "nearest_state": "WA", "country_code": "us", "nearest_lat": 47.6062095}, "start_epoch": 1550622574, "end_engine_hrs": 166291, "assignee_person_type": null, "trip_id": 1550622574, "asset_id": 6519, "start_odometer": 35366364, "start_engine_hrs": 166291, "last_known_driver_id": 2321, "end_distance_since_last_fix": -1, "end_position": "01010000A0E6100000815369D578955EC08C0EED084CCD47400000000000000000", "end_odometer": 35366364, "end_epoch": 1550622582, "assignee_person_id": null, "start_geolocation": {"nearest_city": "Seattle", "nearest_lon": -122.3320708, "nearest_distance": 911.1300968188009, "nearest_state": "WA", "country_code": "us", "nearest_lat": 47.6062095}, "assignment_status_id": 2, "start_accum_odo": -1, "start_position": "01010000A0E6100000815369D578955EC08C0EED084CCD47400000000000000000", "start_lat": 47.6038829, "trip_state_reason": "NOT_LOGGED_IN", "assignment_status_ts": null, "end_lon": -122.3355001, "start_lon": -122.3355001, "end_lat": 47.6038829, "end_accum_odo": -1, "start_distance_since_last_fix": -1, "end_accum_hrs": -1, "start_accum_hrs": -1}',
            'source': 'mmw'
          },
          'dcode_name': 'MISSING_REQUIRED_DATA',
          'driver_ts': '2019-02-19 16:29:34',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550622574,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': '35272f85-05ab-49ac-8951-a038b71024d1',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:34',
          'location': '1mi SW WA Seattle',
          'odo': 35366364,
          'oid': '35272f85-05ab-49ac-8951-a038b71024d1',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'DG/MAL created from UDL',
          'data': {
            'condition': 'DG/MAL created from UDL',
            'dcode': 2,
            'debug_info': '{"trip_state_id": 4, "end_geolocation": {"nearest_city": "Seattle", "nearest_lon": -122.3320708, "nearest_distance": 911.1300968188009, "nearest_state": "WA", "country_code": "us", "nearest_lat": 47.6062095}, "start_epoch": 1550622457, "end_engine_hrs": 166291, "assignee_person_type": null, "trip_id": 1550622457, "asset_id": 6519, "start_odometer": 35366364, "start_engine_hrs": 166291, "last_known_driver_id": 2364, "end_distance_since_last_fix": -1, "end_position": "01010000A0E6100000815369D578955EC08C0EED084CCD47400000000000000000", "end_odometer": 35366364, "end_epoch": 1550622574, "assignee_person_id": null, "start_geolocation": {"nearest_city": "Seattle", "nearest_lon": -122.3320708, "nearest_distance": 707.7051745998613, "nearest_state": "WA", "country_code": "us", "nearest_lat": 47.6062095}, "assignment_status_id": 2, "start_accum_odo": -1, "start_position": "01010000A0E61000009D71D01470955EC049D16F044ECD47400000000000000000", "start_lat": 47.6039434, "trip_state_reason": "NOT_LOGGED_IN", "assignment_status_ts": null, "end_lon": -122.3355001, "start_lon": -122.3349659, "end_lat": 47.6038829, "end_accum_odo": -1, "start_distance_since_last_fix": 0, "end_accum_hrs": -1, "start_accum_hrs": -1}',
            'source': 'mmw'
          },
          'dcode_name': 'ENGINE_SYNCH',
          'driver_ts': '2019-02-19 16:29:34',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550622574,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': 'd2daaf7f-341e-43f9-88ce-ce450bc3f3c6',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:34',
          'location': '1mi SW WA Seattle',
          'odo': 35366364,
          'oid': 'd2daaf7f-341e-43f9-88ce-ce450bc3f3c6',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:29:32',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622572,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': 'acaea2c2-dbc4-4002-8a74-4e3b92ab516f',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:29:32',
          'location': None,
          'odo': 0,
          'oid': 'acaea2c2-dbc4-4002-8a74-4e3b92ab516f',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': 200,
          'accum_odo': 100,
          'comments': 'njjjjj',
          'data': {
            'auto_d_end': '{"edit": {"event_record_status": 1, "oid": "d5a50600-ad0c-4682-9d68-6627fbbe2434", "update_epoch": null, "update_user_id": null}, "core": {"asset_id": 11588, "driver_gtc_id": 2321, "event_code": 101, "engine_hrs": -1, "event_type": 1, "lon": -122.33562, "epoch": 1550622402, "accum_hrs": null, "accum_odo": null, "distance_since_last_fix": 4294967295, "reduced_precision": false, "odo": 0, "lat": 47.6048, "event_record_origin": 2, "id": "d5a50600-ad0c-4682-9d68-6627fbbe2434"}, "data": {"user_notes": "jjjjj", "manual_odo": 5555, "manual_loc": "jjjjh"}}',
            'manual_loc': 'trews',
            'user_notes': 'njjjjj'
          },
          'driver_ts': '2019-02-19 16:24:16',
          'editable_fields': [],
          'engine_hrs': 200,
          'epoch': 1550622256,
          'event_code_id': 3,
          'event_code_name': 'DRIVING',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_record_status_id': 5,
          'event_record_status_name': 'REASSIGNING',
          'event_type_id': 1,
          'event_type_name': 'DUTY_STATUS',
          'has_pending_edits': False,
          'id': '2f1e50d1-5928-431a-9ea6-ba59e4476dfd',
          'is_editable': False,
          'is_manual_loc': True,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:24:16',
          'location': 'trews',
          'odo': 100,
          'oid': '12ea4abe-5c91-4a24-b5ce-8a3bc29ae0f0',
          'reduced_precision': False,
          'update_epoch': 1550622420,
          'update_user_id': 2364
        },
        {
          'accum_hrs': 200,
          'accum_odo': 100,
          'comments': None,
          'data': {
            'co_driver_first_name': 'Ydorb',
            'co_driver_gtc_id': 2364,
            'co_driver_last_name': 'Coleman',
            'co_driver_license': '838383',
            'co_driver_license_jurisdiction': 'WA',
            'link_id': 'f24848f9-e36e-4ef2-a294-7709df4c6236'
          },
          'driver_ts': '2019-02-19 16:24:09',
          'editable_fields': [],
          'engine_hrs': 200,
          'epoch': 1550622249,
          'event_code_id': 7,
          'event_code_name': 'CO_DRIVER_START',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 103,
          'event_type_name': 'METADATA',
          'has_pending_edits': False,
          'id': '212b4cd6-49f0-4056-9e77-bec843d859ca',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:24:09',
          'location': None,
          'odo': 100,
          'oid': '212b4cd6-49f0-4056-9e77-bec843d859ca',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'Missing Odometer.',
          'data': {
            'condition': 'Missing Odometer.',
            'dcode': 2,
            'debug_info': '29d792f6-ab2b-46bf-98aa-d99a0881dc14',
            'source': 'tablet'
          },
          'dcode_name': 'ENGINE_SYNCH',
          'driver_ts': '2019-02-19 16:23:55',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622235,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': '7ecd5545-7bb3-41ba-9a3d-b51d86232243',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:23:55',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '7ecd5545-7bb3-41ba-9a3d-b51d86232243',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'Missing Odometer, Location data, Accumulated Engine Hours, Accumulated Odometer.',
          'data': {
            'condition': 'Missing Odometer, Location data, Accumulated Engine Hours, Accumulated Odometer.',
            'dcode': 3,
            'debug_info': '29d792f6-ab2b-46bf-98aa-d99a0881dc14',
            'source': 'tablet'
          },
          'dcode_name': 'MISSING_REQUIRED_DATA',
          'driver_ts': '2019-02-19 16:23:55',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622235,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': '175b27c5-c9da-440a-8e17-a4e2aefdf94a',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:23:55',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '175b27c5-c9da-440a-8e17-a4e2aefdf94a',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:23:55',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622235,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '29d792f6-ab2b-46bf-98aa-d99a0881dc14',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:23:55',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '29d792f6-ab2b-46bf-98aa-d99a0881dc14',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:20:25',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550622025,
          'event_code_id': 2,
          'event_code_name': 'LOGOUT',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': 'aa340e49-256f-4dc8-ab67-078a2e1f3d63',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:20:25',
          'location': None,
          'odo': 0,
          'oid': 'aa340e49-256f-4dc8-ab67-078a2e1f3d63',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'fhsjsl',
          'data': {
            'manual_odo': 456,
            'user_notes': 'fhsjsl'
          },
          'driver_ts': '2019-02-19 16:15:25',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621725,
          'event_code_id': 1,
          'event_code_name': 'OFF_DUTY',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_record_status_id': 1,
          'event_record_status_name': 'ACTIVE',
          'event_type_id': 1,
          'event_type_name': 'DUTY_STATUS',
          'has_pending_edits': False,
          'id': 'f90be327-0be2-4fac-9add-4eff68c721fa',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': True,
          'local_ts': '2019-02-19 16:15:25',
          'location': 'WA Seattle',
          'odo': 456,
          'oid': 'f90be327-0be2-4fac-9add-4eff68c721fa',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'Failed:  due to a validation error and was rejected by FMCSA.',
          'data': {
            'condition': 'Failed:  due to a validation error and was rejected by FMCSA.',
            'dcode': 4,
            'debug_info': '1:DATATRANS:1550621659807:-1:{"driver_gtc_id":2321,"failure_reason":"FMCSA_ERROR","req_id":"f42cc6fc-69f8-40cc-8077-6b6c9314b70e","success":false,"test":true}',
            'source': 'tablet'
          },
          'dcode_name': 'DATA_TRANSFER',
          'driver_ts': '2019-02-19 16:14:19',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550621659,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': '74f4bc93-d875-42c7-9918-2e41da8af88c',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:14:19',
          'location': None,
          'odo': 0,
          'oid': '74f4bc93-d875-42c7-9918-2e41da8af88c',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'dgdgdh',
          'data': {
            'manual_odo': 555,
            'user_notes': 'dgdgdh'
          },
          'driver_ts': '2019-02-19 16:12:40',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621560,
          'event_code_id': 1,
          'event_code_name': 'OFF_DUTY',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_record_status_id': 1,
          'event_record_status_name': 'ACTIVE',
          'event_type_id': 1,
          'event_type_name': 'DUTY_STATUS',
          'has_pending_edits': False,
          'id': '8cb5b3a9-80af-474f-a105-486abb7787b0',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': True,
          'local_ts': '2019-02-19 16:12:40',
          'location': 'WA Seattle',
          'odo': 555,
          'oid': '8cb5b3a9-80af-474f-a105-486abb7787b0',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': 200,
          'accum_odo': 100,
          'comments': 'Missing Location data.',
          'data': {
            'condition': 'Missing Location data.',
            'dcode': 3,
            'debug_info': 'ae2ec2cd-13ea-46a9-a59e-aea4583d896c',
            'source': 'tablet'
          },
          'dcode_name': 'MISSING_REQUIRED_DATA',
          'driver_ts': '2019-02-19 16:11:33',
          'editable_fields': [],
          'engine_hrs': 200,
          'epoch': 1550621493,
          'event_code_id': 3,
          'event_code_name': 'DIAGNOSTIC_SET',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 7,
          'event_type_name': 'DIAG_MAL',
          'has_pending_edits': False,
          'id': '3dcb89fd-faf3-4311-a5e2-063829bda514',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:11:33',
          'location': None,
          'odo': 100,
          'oid': '3dcb89fd-faf3-4311-a5e2-063829bda514',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': 200,
          'accum_odo': 100,
          'comments': None,
          'data': {
            'co_driver_first_name': 'Ydorb',
            'co_driver_gtc_id': 2364,
            'co_driver_last_name': 'Coleman',
            'co_driver_license': '838383',
            'co_driver_license_jurisdiction': 'WA',
            'link_id': 'd6eb32b2-d0b7-4896-9e79-bd08ae6d1326'
          },
          'driver_ts': '2019-02-19 16:11:25',
          'editable_fields': [],
          'engine_hrs': 200,
          'epoch': 1550621485,
          'event_code_id': 7,
          'event_code_name': 'CO_DRIVER_START',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 103,
          'event_type_name': 'METADATA',
          'has_pending_edits': False,
          'id': '80f1c4b0-1429-4086-bcf5-36ee5394ef89',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:11:25',
          'location': None,
          'odo': 100,
          'oid': '80f1c4b0-1429-4086-bcf5-36ee5394ef89',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:11:12',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550621472,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '2a811612-bf1d-43cb-b533-d151a2028945',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:11:12',
          'location': None,
          'odo': 0,
          'oid': '2a811612-bf1d-43cb-b533-d151a2028945',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:11:06',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621466,
          'event_code_id': 2,
          'event_code_name': 'LOGOUT',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '76cb2c19-e419-4363-95c9-6315698db489',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:11:06',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '76cb2c19-e419-4363-95c9-6315698db489',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:08:00',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621280,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': 'af656e77-59fe-49da-9876-1d9fafd079b2',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:08:00',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': 'af656e77-59fe-49da-9876-1d9fafd079b2',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:07:52',
          'editable_fields': [],
          'engine_hrs': None,
          'epoch': 1550621272,
          'event_code_id': 2,
          'event_code_name': 'US_PROPERTY_70',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_record_status_id': 1,
          'event_record_status_name': 'ACTIVE',
          'event_type_id': 102,
          'event_type_name': 'RULESET_CHANGE',
          'has_pending_edits': False,
          'id': '3eff089d-676a-4d8c-b1cc-597415cf1178',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:07:52',
          'location': None,
          'odo': 0,
          'oid': '3eff089d-676a-4d8c-b1cc-597415cf1178',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:07:49',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621269,
          'event_code_id': 2,
          'event_code_name': 'LOGOUT',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '30e0d22d-352b-4480-8ada-c232ad398a16',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:07:49',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '30e0d22d-352b-4480-8ada-c232ad398a16',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'data': {
            'asset_no': 'Yash_8584263',
            'has_manual_pun': False,
            'license_plate_no': '',
            'pun': '717',
            'vin': ''
          },
          'driver_ts': '2019-02-19 16:07:44',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621264,
          'event_code_id': 1,
          'event_code_name': 'ASSET_CHANGE',
          'event_record_origin_id': 1,
          'event_record_origin_name': 'SYSTEM',
          'event_type_id': 104,
          'event_type_name': 'ASSET_CHANGE',
          'has_pending_edits': False,
          'id': 'a8f3a872-abd5-4121-b37f-0d5039532a1f',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:07:44',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': 'a8f3a872-abd5-4121-b37f-0d5039532a1f',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': None,
          'driver_ts': '2019-02-19 16:07:39',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621259,
          'event_code_id': 1,
          'event_code_name': 'LOGIN',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_type_id': 5,
          'event_type_name': 'AUTH_STATUS',
          'has_pending_edits': False,
          'id': '80ccbd10-e016-4b38-a952-6c87d0bfe26b',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': False,
          'local_ts': '2019-02-19 16:07:39',
          'location': 'WA Seattle',
          'odo': 0,
          'oid': '80ccbd10-e016-4b38-a952-6c87d0bfe26b',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        },
        {
          'accum_hrs': None,
          'accum_odo': None,
          'comments': 'dhndfgjsyt',
          'data': {
            'manual_odo': 15454,
            'user_notes': 'dhndfgjsyt'
          },
          'driver_ts': '2019-02-19 16:04:19',
          'editable_fields': [],
          'engine_hrs': 166291,
          'epoch': 1550621059,
          'event_code_id': 1,
          'event_code_name': 'OFF_DUTY',
          'event_record_origin_id': 2,
          'event_record_origin_name': 'DRIVER',
          'event_record_status_id': 1,
          'event_record_status_name': 'ACTIVE',
          'event_type_id': 1,
          'event_type_name': 'DUTY_STATUS',
          'has_pending_edits': False,
          'id': '746d9079-3814-4a7d-93da-1561b45094ba',
          'is_editable': False,
          'is_manual_loc': False,
          'is_manual_odo': True,
          'local_ts': '2019-02-19 16:04:19',
          'location': 'WA Seattle',
          'odo': 15454,
          'oid': '746d9079-3814-4a7d-93da-1561b45094ba',
          'reduced_precision': False,
          'update_epoch': None,
          'update_user_id': None
        }
    ]

    draw_log_events(pdf, event_list)

    # Save PDF
    pdf.output('outputs/tuto1.pdf', 'F')
