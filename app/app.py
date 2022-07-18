import pandas as pd
def handler(event, context): 
    print("Hello World.")
    print(f"You've imported Pandas version {pd.__version__}.")
    return {"message": "Hey good lookin'."}
    