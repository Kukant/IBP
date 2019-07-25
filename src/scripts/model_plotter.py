from keras.utils import plot_model
from keras.models import load_model

models_path = "/Users/kuky/Google Drive/tmp/logs257/models/"


# model_names = ["random-2-c-32-n-0-d-1563984974", "random-3-c-32-n-0-d-1563985028", "random-3-c-64-n-0-d-1563985319"]
model_names = ["categorical-3-conv-32-nodes-25-epochs-1563989797"]
for model_name in model_names:
    model = load_model(models_path + model_name + ".model")
    plot_model(model, to_file=model_name.split(".")[0] + '_graph.png',
               show_shapes=True, show_layer_names=False)