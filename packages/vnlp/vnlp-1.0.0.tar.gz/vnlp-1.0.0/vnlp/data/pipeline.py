class AnnotationPipeline:

    def __init__(self, stages=None):
        self.stages = stages or []

    def __call__(self, element):
        ann = {'orig': element}
        for stage in self.stages:
            stage(ann)
        return ann
