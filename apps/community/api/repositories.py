from apps.community.models import TalentPool


class TalentPoolRepository:
    DEFAULT_QS = TalentPool.objects.filter(status=TalentPool.Status.PUBLİSHED).order_by('-published_at')

    def __init__(self):
        self.model = TalentPool

    def get_by_sector(self, sector, qs=DEFAULT_QS):
        return qs.filter(sector__slug=sector)
    
    def get_by_position(self, position, qs=DEFAULT_QS):
        return qs.filter(position__slug=position)
    
    def get_by_level(self, level, qs=DEFAULT_QS):
        return qs.filter(level__slug=level)
    
    def get_by_job_type(self, type, qs=DEFAULT_QS):
        job_type = 2 if type == 'closed' else 1
        return qs.filter(job_type=job_type)
    
    def get_by_work_location(self, work_location, qs=DEFAULT_QS):
        return qs.filter(work_location__icontains=work_location)