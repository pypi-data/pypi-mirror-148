import pandas
from pandas import DataFrame, Series

from clime_productivity.args import mainArgs
from clime_productivity.version import version

def calculateProductivity(df: DataFrame) -> DataFrame:
    divedend: int = df["author_days_since_0"].max()
    daysSince0: Series = df["author_days_since_0"].unique()

    data: list = []

    day: int
    for day in range(daysSince0.max() + 1):
        temp: dict = {}

        productivity: float = (
            df[df["author_days_since_0"] == day]["delta_lines_of_code"].abs().sum()
            / divedend
        )

        temp["days_since_0"] = day
        temp["productivity"] = productivity

        data.append(temp)

    return DataFrame(data)


def main():
    args = mainArgs()

    if args.version:
        print(f"clime-productivity-compute version {version()}")
        quit(0)

    df: DataFrame = pandas.read_json(args.input).T
    calculateProductivity(df).to_json(args.output, indent=4)


if __name__ == "__main__":
    main()
