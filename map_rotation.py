from datetime import datetime as dt
import pytz

def map_at_time(query_time_str):
    ISO8601_FORMAT = "%Y-%m-%d %H:%M:%S %z"
    ROTATION_START_TIME_STR = "2023-08-08 10:00:00 -07:00"
    ROTATION_DURATION = 27000
    ROTATION_MAPS = ["Broken Moon", "Kings Canyon", "Olympus"]
    DURATION_TO_MAP = {
        range(0, 5400): ROTATION_MAPS[0],
        range(5400, 10800): ROTATION_MAPS[1],
        range(10800, 16200): ROTATION_MAPS[2],
        range(16200, 19800): ROTATION_MAPS[0],
        range(19800, 23400): ROTATION_MAPS[1],
        range(23400, 27000): ROTATION_MAPS[2]
    }

    # Calculate elapsed time
    rotation_start_time = dt.strptime(ROTATION_START_TIME_STR, ISO8601_FORMAT)
    query_time = dt.strptime(query_time_str, ISO8601_FORMAT)
    elapsed_time = (query_time - rotation_start_time).total_seconds()

    # Calculate Map and Duration
    data = { "range": range, "map": None, "duration": None }
    normalized_elapsed_time = int(elapsed_time % ROTATION_DURATION)
    for duration_range, map in DURATION_TO_MAP.items():
        if normalized_elapsed_time not in duration_range: continue
        data["range"] = duration_range
        data["map"] = map
        data["duration"] = duration_range.stop - duration_range.start
        break

    query_time_since_midnight = query_time.hour * 3600 + query_time.minute * 60 + query_time.second

    # Calculate start and end times
    start_time = query_time_since_midnight - (normalized_elapsed_time - data["range"].start)
    end_time = start_time + data["duration"]
    remaining_time = data["range"].stop - normalized_elapsed_time

    # Convert to HH:MM
    start_time_str = f"{start_time // 3600:02d}:{(start_time % 3600) // 60:02d}"
    end_time_str = f"{end_time // 3600:02d}:{(end_time % 3600) // 60:02d}"
    remaining_time_str = f"{remaining_time // 3600:02d}:{(remaining_time % 3600) // 60:02d}:{remaining_time % 60:02d}"

    # Print information
    print(f"Map: {data['map']}")
    print(f"{start_time_str} - {end_time_str}")
    print(f"Time remaining: {remaining_time_str}")

def main():
    map_at_time(dt.now(pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S %z"))

if __name__ == "__main__":
    main()