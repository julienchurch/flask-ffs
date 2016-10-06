import os
from uuid import uuid4
from werkzeug import secure_filename
from flask import current_app as app

class FFSMixin(object):

  @property
  def ffs_model_category(self):
    raise NotImplementedError

  default_prefix = '^'
  valid_exts = ['jpg', 'gif', 'png']

  def _make_image_dir_if_not_exists(self):
    if not os.path.isdir(self.images_dir):
      try:
        os.makedirs(self.images_dir)
      except OSError as exception:
        if exception.errno != errno.EEXIST:
          raise

  def _make_uuid(self):
    return str(uuid4())

  def _starts_with_default_prefix(self, filename):
    return filename.find(self.default_prefix) == 0

  def _strip_default_prefix(self, filename):
    if self._starts_with_default_prefix(filename):
      return filename.replace(self.default_prefix, '', 1)
    return filename

  def _add_uuid(self, filename):
    uuid_str = self._make_uuid()
    base, ext = os.path.splitext(filename)
    base_with_rand_str = '.'.join([base, uuid_str])
    return ''.join([base_with_rand_str, ext])

  def _add_default_prefix(self, filename):
    if self._starts_with_default_prefix(filename):
      return filename
    return self.default_prefix + filename

  def _purge_defaults(self):
    filenames = os.listdir(self.images_dir)
    for filename in filenames:
      src = os.path.join(self.images_dir, filename)
      dst = os.path.join(self.images_dir, self._strip_default_prefix(filename))
      os.rename(src, dst)

  def _get_default_filename(self):
    filenames = os.listdir(self.images_dir)
    for filename in filenames:
      if self._starts_with_default_prefix(filename):
        return filename
    raise Exception('No default image has been set for this object.')

  def _get_supplementary_filenames(self):
    filenames = os.listdir(self.images_dir)
    for filename in filenames:
      if not self._starts_with_default_prefix(filename):
        yield filename

  def has_valid_ext(self, filename):
    _, ext = os.path.splitext(filename)
    return ext.lower()[1:] in self.valid_exts

  def make_unique_filename(self, filename):
    return self._add_uuid(secure_filename(filename))

  def save_default_image(self, image):
    if self.has_valid_ext(image.filename):
      unique_filename = self.make_unique_filename(image.filename)
      filename = self._add_default_prefix(unique_filename)
      self._make_image_dir_if_not_exists()
      self._purge_defaults()
      save_path = os.path.join(self.images_dir, filename)
      image.save(save_path)
    else: raise

  def save_supplementary_image(self, image):
    if self.has_valid_ext(image.filename):
      filename = self.make_unique_filename(image.filename)
      self._make_image_dir_if_not_exists()
      save_path = os.path.join(self.images_dir, filename)
      image.save(save_path)
    else: raise

  @property
  def ffs_model_id(self):
    try:
      return secure_filename(str(self.id))
    except: 
      print('\n\
To save an image associated with this object, you must \
provide a means of identifying it on the file system. By \
default an `id` attribute is tried; when if fails, the \
`ffs_model_id` attribute must be set directly on the class \
that inherits from `ImageMixin`.\n')
      raise 

  @property
  def images_url(self):
    return os.path.join(app.config['IMAGES_URL'], self.ffs_model_category, self.ffs_model_id)

  @property
  def images_dir(self):
    return os.path.join(app.config['IMAGES_DIR'], self.ffs_model_category, self.ffs_model_id)

  @property
  def default_image(self):
    return os.path.join(self.images_dir, self._get_default_filename())

  @default_image.setter
  def default_image(self, new_image):
    self.save_default_image(new_image)

  @property
  def supplementary_images(self):
    for filename in self._get_supplementary_filenames():
      yield os.path.join(self.images_dir, filename)

  @property
  def url_for_default_image(self):
    filename = self._get_default_filename()
    if filename:
      return os.path.join(self.images_url, filename)

  @property
  def urls_for_supplementary_images(self):
    for filename in self._get_supplementary_filenames():
      if filename:
        yield os.path.join(self.images_url, filename)

