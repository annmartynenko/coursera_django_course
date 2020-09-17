import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Site, Iso, Region, States, Category


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Site.objects.all().delete()
    Iso.objects.all().delete()
    Region.objects.all().delete()
    States.objects.all().delete()
    Category.objects.all().delete()

    for row in reader:
        print(row)

        c, created = Category.objects.get_or_create(name=row[7])
        s, created = States.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        i, created = Iso.objects.get_or_create(name=row[10])

        try:
            y = int(row[3])
            ah = float(row[6])
        except:
            y = None
            ah = 0

        site = Site(name=row[0], description=row[1], justification=row[2], year=y, longitude=row[4], latitude=row[5], area_hectares=ah, category=c, states=s, region=r, iso=i)
        site.save()