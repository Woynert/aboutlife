PUT /close_tabs_reset

DELETE /close_tabs

GET /state

    response:
    ```json
    {
        "state": int,
        "end_time": int,
        "task_info": string,
        "close_tabs": bool,
        "sticky_discrete": bool,
    }
    ```

PUT /start_tomato_break

PUT /start_work_session

    argument:
    ```json
    {
        "task_info": str
        "duration": int (minutes)
        "network_required": bool
        "sticky_discrete": bool
    }
    ```

DELETE /shutdown_system

