from manager import main_manager
def main():
    main_manager()

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        print("\nbye!🙋")