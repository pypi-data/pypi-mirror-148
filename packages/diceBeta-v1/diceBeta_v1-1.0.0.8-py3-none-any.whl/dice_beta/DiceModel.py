from .deepLearning.inference import Initialize, Inference


class TextModel:
    def __init__(self, model_name, class_dict_dir, model_weight_dir):
        Initialize(model_name, class_dict_dir, model_weight_dir)

    def inference(k, text):
        return Inference(k, text)
