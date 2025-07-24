# Exercise 1: Meanings, Values, Relations, and Advantages
import logging, sys

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s -%(levelname)s - %(message)s',
    stream=sys.stdout
)

def processData():
    try:
        pathFile = "../input.dat"
        try:
            with open(pathFile, 'r') as f:
                for line in f:
                    number = int(line)
                    if number < 0: 
                        logging.warning(f"Hardware fault")
                        continue
                    if number == 0:
                        # sys.exit(f"{number} values can broke divisions")
                        raise ValueError(f"{number} values can broke divisions")
                    logging.info(f"The signal: {number}, and its square: {number**2}")
        except TypeError:
            logging.warning(f"Line {line} is not correctly valued")
        except ValueError as e:
            logging.error(f"Signal value as 0 with error as {e}")
            sys.exit()
        except Exception as e:
            logging.warning(f"Unexpected exception ({e}) for line {line}")
    except FileNotFoundError:
        logging.error(f"File {pathFile} does not exists")
        sys.exit()

if __name__ == "__main__":
    processData()
