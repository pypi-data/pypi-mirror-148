import wget
import tarfile
import os


def TF2_download_model(download_url,model_folder_name,model_file_name):
    if os.path.exists(os.path.join(os.getcwd()+ '\\TF2\TF2_model\\'+model_folder_name)):
        print("The required model folder already exist")
        model_dir= os.getcwd() + '\\TF2\TF2_model\\'+model_folder_name+"\\saved_model"
    elif os.path.exists(os.path.join(os.getcwd()+ '\\TF2\TF2_model\\'+model_file_name)):
        print("The required model file already exist")
        tar = tarfile.open(os.path.join(os.getcwd()+ '\\TF2\TF2_model\\'+model_file_name))
        foldername = tar.getnames()[0]
        tar.extractall("TF2\TF2_model")
        tar.close            
        model_dir= os.getcwd() + '\\TF2\TF2_model\\'+foldername+"\\saved_model"
    else:
        print(download_url)
        raw_filename = wget.download(download_url,out=os.getcwd() + '\\TF2\TF2_model\\')
        print(raw_filename)
        tar = tarfile.open(raw_filename)
        foldername = tar.getnames()[0]
        tar.extractall("TF2\TF2_model")
        tar.close            
        model_dir= os.getcwd() + '\\TF2\TF2_model\\'+foldername+"\\saved_model"
    return model_dir

# def detectron_download_model(model,model_config_download_url,model_download_url,model_config_filename,model_name):
#     if os.path.exists(os.path.join(os.getcwd()+ '\\detectron\detectron_models\\'+model)):
#         detection_model_config =  os.getcwd() + '\\detectron\detectron_models\\'+model+'\\'+model_config_filename
#         detection_model_dir = os.getcwd() + '\\detectron\detectron_models\\'+model+'\\'+model_name
#         print("Detection Model_Name  Directory:",detection_model_dir)
#         print("Detection Model_Name Config file:",detection_model_config)
#     else:
#         os.mkdir(os.path.join(os.getcwd()+ '\\detectron\detectron_models\\'+model))
#         wget.download(model_config_download_url,out=os.path.join(os.getcwd()+ '\\detectron\detectron_models\\'+model))
#         wget.download(model_download_url,out=os.path.join(os.getcwd()+ '\\detectron\detectron_models\\'+model))
#         detection_model_config =  os.getcwd() + '\\detectron\detectron_models\\'+model+'\\'+model_config_filename
#         detection_model_dir = os.getcwd() + '\\detectron\detectron_models\\'+model+'\\'+model_name
#         print("Detection Model_Name  Directory:",detection_model_dir)
#         print("Detection Model_Name Config file:",detection_model_config)
#     return detection_model_dir,detection_model_config