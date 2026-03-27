# Guide to `Power BI`

## Sort the order of visualizations using a custom sort

- Open up Power Query editor for table containing the column to set a custom order.
- Use the following M code to create a new column containing custom ordering:
    - `order_column_name`: replace `column_name` with the column's name.
    - `previous_step_name`: replace with the actual previous step's name.
    - `COLUMN_NAME_ORDER`: replace `COLUMN_NAME` with the column's name.
    - `COLUMN_NAME`: replace with the column to be sorted.
    - `Value1`: replace with the actual value in the column, repeat for all rows.
    - Setting `else null` is option to catch if an unexpected value occurs.

```M
// Create a custom order for a column
order_column_name = Table.AddColumn(
    previous_step_name, 
    "COLUMN_NAME_ORDER", 
    each 
        if [COLUMN_NAME] = "Value1" then 1
        else if [COLUMN_NAME] = "Value2" then 2
        else if [COLUMN_NAME] = "Value3" then 3
        else if [COLUMN_NAME] = "Value4" then 4
        else if [COLUMN_NAME] = "n/a" then 5
        else null
    ),
```

- After exiting Power Query, navigate to `Table view`.
- Select the table with the column to be sorted.
- Select the column to be sorted and in the ribbon, select `Sort by column` drop-down and select the order column.
- *Another option is to create a table with one column ordered by numbers and the other containing the categories. Then confirm a relationship between categories has been established in `Model view`. I believe the former method is better.*

References

- [Power BI - Custom Sorting in 3 Easy Steps!](https://www.youtube.com/watch?v=4xapOrfLvbg)