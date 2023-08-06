class JobGroup:
    def __init__(self, client):
        self.client = client

    def list_job_group(self, program_id, start_date=None, end_date=None, search_key=None, sort_by='id', reverse=True,
                       page=None, per_page=50):
        params = {
            'program_id': program_id
        }
        if start_date is not None:
            params['start_time'] = start_date.strftime("%Y-%m-%d")
        if end_date is not None:
            params['end_time'] = end_date.strftime("%Y-%m-%d")
        if search_key is not None:
            params['search_key'] = search_key
        if sort_by is not None:
            params['sortby'] = sort_by
        if not reverse:
            params['reverse'] = 0
        if page is not None:
            pass
            params['page'] = page
        else:
            params['page'] = 0
        if per_page:
            params['per_page'] = per_page
        else:
            params['per_page'] = 50
        data = self.client.get("/data/job_groups", params=params)
        return data

    def list_job_group_by_number(self, program_id, number, start_date=None, end_date=None, search_key=None,
                                 sort_by=None,
                                 reverse=True):
        per_page = 50
        jobgroup_list = []
        data = self.list_job_group(program_id, start_date=start_date, end_date=end_date, search_key=search_key,
                                   sort_by=sort_by, reverse=reverse, page=0, per_page=per_page)
        total = data['total']
        per_page = data['per_page']
        page_number = 0
        while page_number * per_page < total:
            page_number = page_number + 1
            if page_number > 1:
                data = self.list_job_group(program_id, start_date=start_date, end_date=end_date, search_key=search_key,
                                           sort_by=sort_by, reverse=reverse, page=page_number, per_page=per_page)
            for each in data['items']:
                jobgroup_list.append(each)
                if len(jobgroup_list) >= number:
                    return jobgroup_list
        return jobgroup_list

    def terminate(self, job_group_id):
        data = self.client.post(f"/data/job_group/{job_group_id}/terminate")
        return data

    def delete(self, job_group_id):
        data = self.client.post(f"/data/job_group/{job_group_id}/del")
        return data
