from src.orchestrator import *

def main():
    while True:
        
        query = input("> ")

        print(run_query(query))
        # send query to agent here

if __name__ == "__main__":
    main()