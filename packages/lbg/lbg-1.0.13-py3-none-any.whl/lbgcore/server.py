class Server:
    def __init__(self, client):
        self.client = client

    def list_server(self, program_id):
        data = self.client.get('/machine/list', params={'program_id': program_id})
        return data['items']

    def stop(self, machine_id):
        data = self.client.post(f'/machine/{machine_id}/stop')
        return data

    def restart(self, machine_id):
        data = self.client.post(f'/machine/{machine_id}/restart')
        return data

    def delete(self, machine_id):
        data = self.client.post(f'/machine/{machine_id}/delete')
        return data

    def create(self, image_id, disk_size, memory, cpu, gpu, platform, program_id, name=None):
        post_data = {
            'image_id': image_id,
            'disk_size': disk_size,
            'program_id': program_id,
            'memory': memory,
            'cpu': cpu,
            'gpu': gpu,
            'platform': platform,
            'name': name
        }
        data = self.client.post(f'/machine/create', data=post_data)
        return data

    def to_dev_image(self, machine_id, image_name, comment=''):
        params = {
            'image_name': image_name,
            'machine_id': machine_id,
            'comment': comment
        }
        data = self.client.post(f'/image/snapshot/create', data=params)
        return data
