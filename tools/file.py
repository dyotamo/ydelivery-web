from os.path import join
from csv import DictReader
from tempfile import gettempdir

from werkzeug.utils import secure_filename

from models import db, Brew


def save_csv(form):
    """ An utility function to save a file in the /tmp directory,
    returning its path for further processing """
    csv = form.csv.data
    path = join(gettempdir(), secure_filename(csv.filename))
    csv.save(path)
    return path


def import_csv(f):
    with db.session.no_autoflush:
        csv_reader = DictReader(f, delimiter=',')

        for row in csv_reader:
            product = Brew.query.filter_by(name=row['name']).first()
            if product is None:
                db.session.add(Brew(**row))
            else:
                product.name = row['name']
                product.unit_price = row['unit_price']
                db.session.merge(product)
        db.session.commit()
