import feature_handler
def main():
    print()    
    while True:
        feature_handler.menu()
        print()

try:
    main()
except KeyboardInterrupt:
    exit()
    