from analysis import (
    dataset_summary,
    dataset_columns,
    dataset_head,
    dataset_insights,
    generate_report
)

def ask_ai(question):

    question = question.lower()

    if "summary" in question:

        return dataset_summary()

    elif "columns" in question:

        return dataset_columns()

    elif "sample" in question:

        return dataset_head()

    elif "insights" in question:

        return dataset_insights()

    elif "report" in question:

        return generate_report()

    else:

        return """
Available Commands:

summary
columns
sample
chart
train
insights
report
"""