from app import AirQualityApp


def main():
    app = AirQualityApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user. Goodbye.")