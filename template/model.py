import os
import torch
import torch.optim as optim
from models.ban import BAN
from models.attnet import Attnet
from models.MI_net import MINet
from models.minet import MiNet
from models.sa_abmilp import SA_ABMILP
from template.template import TemplateModel
import tensorboardX as tX
from utils.utils import read_yaml
import os.path as osp

def metric(pred, target):
    pred = torch.ge(pred, 0.5).float()
    correct_num = torch.sum(pred == target).item()
    total_num = target.size(0)
    accuracy = correct_num / total_num
    return 1. - accuracy

def get_criterion(criterion_name):
    if criterion_name == 'cross-entropy':
        criterion = torch.nn.CrossEntropyLoss()
    elif criterion_name == 'binary-cross-entropy':
        criterion = torch.nn.BCELoss()
    elif criterion_name == 'neg-log-likelihood':
        criterion = lambda Y_prob, Y: -1. * (Y * torch.log(Y_prob) + (1. - Y) * torch.log(1. - Y_prob)) 
    else:
        print("ERRORE: nome criterio errato!")
        exit(1)
    return criterion

class Model(TemplateModel):

    def __init__(self, args=None):
        super().__init__()
        self.args = args
        cfg = read_yaml(args.config)

        seed = cfg.General.seed
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

        self.writer = tX.SummaryWriter(log_dir=cfg.General.log_dir, comment=args.model)
        self.train_logger = None
        self.eval_logger = None

        self.step = 0
        self.epoch = 0
        self.best_error = float('Inf')

        self.device = torch.device("cuda" if args.cuda else "cpu")

        self.model, self.optimizer = self.get_model(cfg)
        self.model = self.model.to(self.device)
        self.criterion = get_criterion(cfg.Data[self.args.dataset].Models[self.args.model].criterion)
        self.metric = metric

        self.train_loader = args.train_loader
        self.test_loader = args.test_loader

        self.ckpt_dir = osp.join(cfg.General.ckpt_dir, args.dataset, args.description)
        if not osp.exists(self.ckpt_dir):
            os.mkdir(self.ckpt_dir)
        self.ckpt_dir = osp.join(self.ckpt_dir, args.model)
        
        self.log_per_step = cfg.General.log_per_step
        self.eval_per_epoch = args.eval_per_epoch

        self.best_model_path = osp.join(self.ckpt_dir, 'best.pth.tar')

        self.check_init()

    def get_model(self, cfg):
        model_name = self.args.model
        dataset_params = cfg.Data[self.args.dataset]
        assert model_name in ('minet', 'MI_net', 'attnet', 'sa_abmilp')

        input_dim = dataset_params.input_dim
        model_params = dataset_params.Models[model_name]
        if model_name == 'attnet':
            model = Attnet(cfg, input_dim)
            optimizer = optim.SGD(model.parameters(), 
                                    lr=model_params.lr, 
                                    weight_decay=model_params.weight_decay, 
                                    momentum=model_params.momentum, 
                                    nesterov=model_params.nesterov)
        elif model_name == 'sa_abmilp':
            model = SA_ABMILP(cfg, input_dim, self.device)
            optimizer = optim.SGD(model.parameters(), 
                                    lr=model_params.lr, 
                                    weight_decay=model_params.weight_decay, 
                                    momentum=model_params.momentum, 
                                    nesterov=model_params.nesterov)
        elif model_name == 'minet':
            model = MiNet(cfg, input_dim, pooling_mode=model_params.pooling_mode)
            optimizer = optim.SGD(model.parameters(), 
                                    lr=model_params.lr, 
                                    weight_decay=model_params.weight_decay, 
                                    momentum=model_params.momentum, 
                                    nesterov=model_params.nesterov)
        elif model_name == 'MI_net':
            model = MINet(cfg, input_dim, pooling_mode=model_params.pooling_mode)
            optimizer = optim.SGD(model.parameters(), 
                                    lr=model_params.lr, 
                                    weight_decay=model_params.weight_decay, 
                                    momentum=model_params.momentum, 
                                    nesterov=model_params.nesterov)
        else:
            print("ERRORE: nome modello errato!")
            exit(1)
        return model, optimizer
    
    def get_best_model(self):
        assert osp.exists(self.best_model_path)
        best_model = Model(self.args)
        best_model.load_state(self.best_model_path)
        return best_model

    def get_training_features(self, x=None):
        self.model.eval()

        tr_bags = []
        tr_labels = []
        tr_mask = []
        
        with torch.no_grad():
            if x is not None:
                x = x.to(self.device)
                _, emb = self.model(x)
                tr_bags.append(emb)
            else:
                for batch_idx, batch in enumerate(self.train_loader):
                    x, y = batch
                    y = y[0] #BYFLV     
                    x = x.to(self.device)
                    y = y.to(self.device)
                    _, emb = self.model(x)
                    tr_bags.append(emb)
                    tr_labels.append(y)
                    tr_mask += [batch_idx for i in range(x.shape[1])]
        return (tr_bags, tr_labels, tr_mask)



class Model_with_embs(TemplateModel):

    def __init__(self, args=None):
        super().__init__()
        self.args = args
        cfg = read_yaml(args.config)

        seed = cfg.General.seed
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)

        self.writer = tX.SummaryWriter(log_dir=cfg.General.log_dir, comment=args.model)
        self.train_logger = None
        self.eval_logger = None

        self.step = 0
        self.epoch = 0
        self.best_error = float('Inf')

        self.device = torch.device("cuda" if args.cuda else "cpu")

        self.embeddings = args.embeddings

        self.model, self.optimizer = self.get_model(cfg)
        self.model = self.model.to(self.device)
        self.criterion = get_criterion(cfg.Data[self.args.dataset].Models[self.args.model].criterion)
        self.metric = metric

        self.train_loader = args.train_loader
        self.test_loader = args.test_loader

        self.ckpt_dir = osp.join(cfg.General.ckpt_dir, args.dataset, args.description)
        if not osp.exists(self.ckpt_dir):
            os.mkdir(self.ckpt_dir)
        self.ckpt_dir = osp.join(self.ckpt_dir, args.model)
            
        self.log_per_step = cfg.General.log_per_step
        self.eval_per_epoch = args.eval_per_epoch

        self.best_model_path = osp.join(self.ckpt_dir, 'best.pth.tar')

        self.check_init()
    
    def get_model(self, cfg):
        assert self.args.model in ('ban')
        dataset_params = cfg.Data[self.args.dataset]
        input_dim = dataset_params.input_dim
        model_params = dataset_params.Models[self.args.model]

        if self.args.model == 'ban':
            model = BAN(cfg, input_dim, self.args.base_model, self.device, pooling_mode=model_params.pooling_mode, num_references=len(self.embeddings[1]))
            optimizer = optim.SGD(model.parameters(), 
                                    lr=model_params.lr, 
                                    weight_decay=model_params.weight_decay, 
                                    momentum=model_params.momentum, 
                                    nesterov=model_params.nesterov)
        else:
            print("ERRORE: nome modello errato!")
            exit(1)
        return model, optimizer

    def train_loss(self, batch):
        x, y = batch
        y = y[0] #BYFLV
        x = x.to(self.device)
        y = y.to(self.device)
        tr_bags, _, tr_mask = self.embeddings
        pred, _ = self.model(x, tr_bags, tr_mask)
        loss = self.criterion(pred, y)
        return loss, None
    
    def eval_error(self):
        self.model.eval()
        xs, ys, preds = [], [], []
        for batch in self.test_loader:
            x, y = batch
            y = y[0] #BYFLV
            x = x.to(self.device)
            y = y.to(self.device)
            tr_bags, _, tr_mask = self.embeddings
            pred, _ = self.model(x, tr_bags, tr_mask)

            ys.append(y.unsqueeze(0).cpu())
            preds.append(pred.unsqueeze(0).cpu())

        ys = torch.cat(ys, dim=0)
        preds = torch.cat(preds, dim=0)
        error = self.metric(preds, ys)
        return error, None
    
    def inference(self, x):
        x = x.to(self.device)
        tr_bags, _, tr_mask = self.embeddings
        return self.model(x, tr_bags, tr_mask)[0]
    
    def get_best_model(self):
        assert osp.exists(self.best_model_path)
        best_model = Model_with_embs(self.args)
        best_model.load_state(self.best_model_path)
        return best_model