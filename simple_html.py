import os

thisfilepath = os.path.dirname(__file__)

def html_start(title="Solar Pi Gardener"):
    hs = '<!DOCTYPE html>'
    hs += '<!DOCTYPE html><html><head><link rel="manifest" href="pwa/manifest.json"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous"><script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script><title>' + title + '</title></head><body>'
    return hs

def readfile(filename):
    with open(os.path.join(thisfilepath, 'html', filename)) as f:
        return f.read()
    
def getimage(imgfile):
    with open(os.path.join(thisfilepath, 'html', 'img', imgfile), 'rb') as f:
        return f.read()