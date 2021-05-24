import csv


def csv_handler(rawdata):
    try:
        data = [row for row in csv.DictReader(rawdata.decode("utf-8").splitlines())]
    except UnicodeDecodeError:
        data = [row for row in csv.DictReader(rawdata.decode("big5").splitlines())]
    except Exception:
        data = [row for row in csv.DictReader(rawdata.decode("ANSI").splitlines())]
    except:
        return False
    return data
