def fetch_table_data_last_week(table_name):
    try:
        result = supabase.table(table_name).select("*").gte("fecha_creacion", date_one_week_ago).execute()
        if not result.data:
            print(f"No data returned for table {table_name}")
            return []
        return result.data
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []