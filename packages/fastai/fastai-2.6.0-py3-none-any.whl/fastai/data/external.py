# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_data.external.ipynb (unless otherwise specified).

__all__ = ['fastai_cfg', 'fastai_path', 'URLs', 'untar_data']

# Cell
from ..torch_basics import *
from fastdownload import FastDownload
from functools import lru_cache
import fastai.data

# Cell
@lru_cache(maxsize=None)
def fastai_cfg():
    "`Config` object for fastai's `config.ini`"
    return Config(Path(os.getenv('FASTAI_HOME', '~/.fastai')), 'config.ini', create=dict(
        data = 'data', archive = 'archive', storage = 'tmp', model = 'models'))

# Cell
def fastai_path(folder):
    "Path to `folder` in `fastai_cfg`"
    return fastai_cfg().path(folder)

# Cell
class URLs():
    "Global constants for dataset and model URLs."
    LOCAL_PATH = Path.cwd()
    MDL = 'http://files.fast.ai/models/'
    GOOGLE = 'https://storage.googleapis.com/'
    S3  = 'https://s3.amazonaws.com/fast-ai-'
    URL = f'{S3}sample/'

    S3_IMAGE    = f'{S3}imageclas/'
    S3_IMAGELOC = f'{S3}imagelocal/'
    S3_AUDI     = f'{S3}audio/'
    S3_NLP      = f'{S3}nlp/'
    S3_COCO     = f'{S3}coco/'
    S3_MODEL    = f'{S3}modelzoo/'

    # main datasets
    ADULT_SAMPLE        = f'{URL}adult_sample.tgz'
    BIWI_SAMPLE         = f'{URL}biwi_sample.tgz'
    CIFAR               = f'{URL}cifar10.tgz'
    COCO_SAMPLE         = f'{S3_COCO}coco_sample.tgz'
    COCO_TINY           = f'{S3_COCO}coco_tiny.tgz'
    HUMAN_NUMBERS       = f'{URL}human_numbers.tgz'
    IMDB                = f'{S3_NLP}imdb.tgz'
    IMDB_SAMPLE         = f'{URL}imdb_sample.tgz'
    ML_SAMPLE           = f'{URL}movie_lens_sample.tgz'
    ML_100k             = 'https://files.grouplens.org/datasets/movielens/ml-100k.zip'
    MNIST_SAMPLE        = f'{URL}mnist_sample.tgz'
    MNIST_TINY          = f'{URL}mnist_tiny.tgz'
    MNIST_VAR_SIZE_TINY = f'{S3_IMAGE}mnist_var_size_tiny.tgz'
    PLANET_SAMPLE       = f'{URL}planet_sample.tgz'
    PLANET_TINY         = f'{URL}planet_tiny.tgz'
    IMAGENETTE          = f'{S3_IMAGE}imagenette2.tgz'
    IMAGENETTE_160      = f'{S3_IMAGE}imagenette2-160.tgz'
    IMAGENETTE_320      = f'{S3_IMAGE}imagenette2-320.tgz'
    IMAGEWOOF           = f'{S3_IMAGE}imagewoof2.tgz'
    IMAGEWOOF_160       = f'{S3_IMAGE}imagewoof2-160.tgz'
    IMAGEWOOF_320       = f'{S3_IMAGE}imagewoof2-320.tgz'
    IMAGEWANG           = f'{S3_IMAGE}imagewang.tgz'
    IMAGEWANG_160       = f'{S3_IMAGE}imagewang-160.tgz'
    IMAGEWANG_320       = f'{S3_IMAGE}imagewang-320.tgz'

    # kaggle competitions download dogs-vs-cats -p {DOGS.absolute()}
    DOGS = f'{URL}dogscats.tgz'

    # image classification datasets
    CALTECH_101  = f'{S3_IMAGE}caltech_101.tgz'
    CARS         = f'{S3_IMAGE}stanford-cars.tgz'
    CIFAR_100    = f'{S3_IMAGE}cifar100.tgz'
    CUB_200_2011 = f'{S3_IMAGE}CUB_200_2011.tgz'
    FLOWERS      = f'{S3_IMAGE}oxford-102-flowers.tgz'
    FOOD         = f'{S3_IMAGE}food-101.tgz'
    MNIST        = f'{S3_IMAGE}mnist_png.tgz'
    PETS         = f'{S3_IMAGE}oxford-iiit-pet.tgz'

    # NLP datasets
    AG_NEWS                 = f'{S3_NLP}ag_news_csv.tgz'
    AMAZON_REVIEWS          = f'{S3_NLP}amazon_review_full_csv.tgz'
    AMAZON_REVIEWS_POLARITY = f'{S3_NLP}amazon_review_polarity_csv.tgz'
    DBPEDIA                 = f'{S3_NLP}dbpedia_csv.tgz'
    MT_ENG_FRA              = f'{S3_NLP}giga-fren.tgz'
    SOGOU_NEWS              = f'{S3_NLP}sogou_news_csv.tgz'
    WIKITEXT                = f'{S3_NLP}wikitext-103.tgz'
    WIKITEXT_TINY           = f'{S3_NLP}wikitext-2.tgz'
    YAHOO_ANSWERS           = f'{S3_NLP}yahoo_answers_csv.tgz'
    YELP_REVIEWS            = f'{S3_NLP}yelp_review_full_csv.tgz'
    YELP_REVIEWS_POLARITY   = f'{S3_NLP}yelp_review_polarity_csv.tgz'

    # Image localization datasets
    BIWI_HEAD_POSE     = f"{S3_IMAGELOC}biwi_head_pose.tgz"
    CAMVID             = f'{S3_IMAGELOC}camvid.tgz'
    CAMVID_TINY        = f'{URL}camvid_tiny.tgz'
    LSUN_BEDROOMS      = f'{S3_IMAGE}bedroom.tgz'
    PASCAL_2007        = f'{S3_IMAGELOC}pascal_2007.tgz'
    PASCAL_2012        = f'{S3_IMAGELOC}pascal_2012.tgz'

    # Audio classification datasets
    MACAQUES           = f'{GOOGLE}ml-animal-sounds-datasets/macaques.zip'
    ZEBRA_FINCH        = f'{GOOGLE}ml-animal-sounds-datasets/zebra_finch.zip'

    # Medical Imaging datasets
    #SKIN_LESION        = f'{S3_IMAGELOC}skin_lesion.tgz'
    SIIM_SMALL         = f'{S3_IMAGELOC}siim_small.tgz'
    TCGA_SMALL         = f'{S3_IMAGELOC}tcga_small.tgz'

    #Pretrained models
    OPENAI_TRANSFORMER = f'{S3_MODEL}transformer.tgz'
    WT103_FWD          = f'{S3_MODEL}wt103-fwd.tgz'
    WT103_BWD          = f'{S3_MODEL}wt103-bwd.tgz'

    def path(url='.', c_key='archive'):
        "Return local path where to download based on `c_key`"
        fname = url.split('/')[-1]
        local_path = URLs.LOCAL_PATH/('models' if c_key=='model' else 'data')/fname
        if local_path.exists(): return local_path
        return fastai_path(c_key)/fname

# Cell
def untar_data(url, archive=None, data=None, c_key='data', force_download=False):#, extract_func=file_extract, timeout=4):
    "Download `url` to `fname` if `dest` doesn't exist, and extract to folder `dest`"
    d = FastDownload(fastai_cfg(), module=fastai.data, archive=archive, data=data, base='~/.fastai')
    return d.get(url, force=force_download, extract_key=c_key)