from os.path import join
from csv import DictReader
from tempfile import gettempdir
from werkzeug.utils import secure_filename
from models import db, Product


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
            product = Product.query.filter_by(name=row['name']).first()
            if product is None:
                db.session.add(Product(**row))
            else:
                product.name = row['name']
                product.unit_price = row['unit_price']
                product.quantity = row['quantity']
                product.image = row['image']
                db.session.merge(product)
        db.session.commit()
