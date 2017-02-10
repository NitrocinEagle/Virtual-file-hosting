from django.views.generic import FormView

from . import s3
from .forms import FileFieldForm


class FileBrowser(FormView):
    form_class = FileFieldForm
    template_name = 'file_browser.html'

    def get_success_url(self):
        return self.request.get_full_path()

    def get_context_data(self, **kwargs):
        context = super(FileBrowser, self).get_context_data(**kwargs)
        root = self.request.GET.get('root', '')
        objects = s3.get_objects()

        keys = [obj['Key'] for obj in objects['Contents']]

        objects_to_show = []

        keys = filter(lambda x: x.startswith(root), keys)
        keys_in_root_dir = list(map(lambda x: x.replace(root, '').strip('/'), keys))
        # keys_in_root_dir = list(filter(lambda x: x.count('/') or x.count('.'), keys_in_root_dir))

        dirs = {key.split('/', 1)[0] for key in keys_in_root_dir if key.count('/')}

        # Update dirs with empty folders
        dirs.update({key for key in keys_in_root_dir if not key.count('/') and not key.count('.')})

        # Remove from dirs folders with no name (like, '')
        dirs = list(filter(lambda x: x, dirs))

        files = [key for key in keys_in_root_dir if not key.count('/') and key.count('.')]

        for d in dirs:
            objects_to_show.append({
                'name': d,
                'dir': True,
                'dir_link': root + d,
                'edit_link': None
            })

        for f in files:
            objects_to_show.append({
                'name': f,
                'dir': False,
                'dir_link': None,
                'edit_link': None,
                'obj_link': 'https://console.aws.amazon.com/s3/buckets/{}/{}/details?region=us-east-1&tab=overview'.format(
                    s3.bucket_name, root + f)
            })

        context['objects'] = objects_to_show
        context['empty_folder'] = False if files or dirs else True
        context['prev_folder'] = 'None'

        if root.count('/') > 1:
            context['prev_folder'] = root.rstrip('/').rsplit('/', 1)[0] + '/'
        elif root.count('/') == 1:
            context['prev_folder'] = ''

        return context

    def post(self, request, *args, **kwargs):
        root = self.request.GET.get('root', '')
        form = self.get_form()
        if form.is_valid():
            for file in request.FILES.getlist('files'):
                data, key = file, root + file.name
                s3.upload_object(data, key)

        s3.update_objects()
        return super(FileBrowser, self).get(request, *args, **kwargs)
