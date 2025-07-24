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

# Answer the following theoretical questions:
#     Based on the course materials, explain the key difference between a fault and a failure. In this exercise, is the negative number a 
# fault or a failure?
# Answer: is a fault
#     Proprietary Alternative: If this script were deployed as an AWS Lambda function triggered by new lines in a file, how might the 
# platform's behavior for the hardware fault (negative number) and software bug (ZeroDivisionError) differ from your script's behavior? 
# What are the advantages of the managed service approach?
# Answer: using kubernetes managing the function we could have a killed funtion to avoid consequences with the bad signal and then alive it
# again to keep the service available for new signals
#     Open-Source Advantage: What is the primary advantage of implementing this fault tolerance logic yourself in Python, as you have done, 
# versus relying on a proprietary platform's defaults?
# Answer: tech enterprises give highly common patterns for system behaviors, if your system is too unique you should need a combination of
# private services to perform the same behavior you should solve with less python lines, in fact could be impossible with privative services
# the first makes expensive the system and the second forces you to follow too complex or inappropriate standards