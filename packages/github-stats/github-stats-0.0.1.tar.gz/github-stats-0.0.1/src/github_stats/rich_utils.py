from typing import Optional

import pandas as pd
from rich.progress import BarColumn, Progress, TaskID, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table


def get_rich_progress_and_run_id(tasks: list) -> (Progress, TaskID):
    progress = Progress(
        "{task.description}",
        BarColumn(),
        TextColumn("[progress.completed]{task.completed}/{task.total}"),
        "•",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        auto_refresh=False,
    )
    run_id = progress.add_task("[bold blue]Repos", total=len(tasks))

    return progress, run_id


def df_to_table(
    pandas_dataframe: pd.DataFrame,
    rich_table: Table,
    show_index: bool = True,
    index_name: Optional[str] = None,
) -> Table:
    """Convert a pandas.DataFrame obj into a rich.Table obj.
    Args:
        pandas_dataframe (DataFrame): A Pandas DataFrame to be converted to a rich Table.
        rich_table (Table): A rich Table that should be populated by the DataFrame values.
        show_index (bool): Add a column with a row count to the table. Defaults to True.
        index_name (str, optional): The column name to give to the index column. Defaults to None, showing no value.
    Returns:
        Table: The rich Table instance passed, populated with the DataFrame values."""

    if show_index:
        index_name = str(index_name) if index_name else ""
        rich_table.add_column(index_name)

    for column in pandas_dataframe.columns:
        rich_table.add_column(str(column))

    for index, value_list in enumerate(pandas_dataframe.to_numpy()):
        row = [str(index)] if show_index else []
        row += [str(x) for x in value_list.tolist()]
        rich_table.add_row(*row)

    return rich_table
