import torch
from roidata import ResSimRoi, custom_collate
from simodel import SimRes50
import pandas as pd
import torch.nn as nn
import torch.optim as optim
import time
import copy
import pickle

# Train function
def train_model(model, criterion, optimizer, lr_scheduler, num_epochs = 100):
    train_loss = []
    train_acc = []
    val_loss = []
    val_acc = []
    test_loss = []
    test_acc = []
    val_test_loss = []
    val_test_acc = []

    since = time.time()

    best_model = model
    best_acc = 0.0

    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        for phase in ['train', 'val', 'test']:
            if phase == 'train':
                optimizer = lr_scheduler(optimizer, epoch)
                model.train()  # Set model to training mode
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for data in dset_loaders[phase]:
                for _list in data:
                    for tup in _list:
                        inputs, box, label = tup
                        inputs = inputs.unsqueeze(0).type(torch.FloatTensor)
                        inputs, box, label = inputs.to(device), box.to(device), label.to(device).long() # Datasets에서는 64 bit인데 왜 여기서는 32 bit로 바뀔까..일단은 long() 함수는 통해 int64의 Longtensor로 dtype 맞춤

                        optimizer.zero_grad()
                        outputs = model(inputs, box)
                        _, preds = torch.max(outputs.data, 1)
                        loss = criterion(outputs, label)

                        if phase == 'train':
                            loss.backward()
                            optimizer.step()
                        try:
                            running_loss += loss.item()
                            running_corrects += torch.sum(preds == label.data)
                        except:
                            print('unexpected error, could not calculate loss or do a sum.')

        print('trying epoch loss')
        epoch_loss = running_loss / dset_sizes[phase]
        epoch_acc = running_corrects.item() / float(dset_sizes[phase])
        print('{} Loss: {:.4f} Acc: {:.4f}'.format(
            phase, epoch_loss, epoch_acc))

        if phase == 'train':
            train_loss.append(epoch_loss)
            train_acc.append(epoch_acc)

        if phase == 'val':
            val_loss.append(epoch_loss)
            val_acc.append(epoch_acc)

        if epoch_acc > best_acc:
            best_acc = epoch_acc
            best_model = copy.deepcopy(model)
            torch.save(best_model.state_dict(), 'RoI_log/Res_Sim_Best_RoI.pt') # Best model save
            print('new best accuracy = ', best_acc)

        if phase == 'test':
            test_loss.append(epoch_loss)
            test_acc.append(epoch_acc)

        if epoch_acc > best_acc:
            best_acc = epoch_acc
            best_model = copy.deepcopy(model)
            torch.save(best_model.state_dict(), 'RoI_log/Res_Sim_Best_RoI.pt') # Best model save
            print('new best accuracy = ', best_acc)

    val_test_loss.append((val_loss[-1] * dset_sizes['val'] + test_loss[-1] * dset_sizes['test']) / float(dset_sizes['val_test']))
    val_test_acc.append((val_acc[-1] * dset_sizes['val'] + test_acc[-1] * dset_sizes['test']) / float(dset_sizes['val_test']))

    # Store history
    with open('RoI_log/history_1.pickle', 'wb') as f:
        data = {'batch size': {'train' : 64, 'val': 32, 'test' : 32}, 'train_loss': train_loss, 'train_acc': train_acc, 'val_loss': val_loss, 'val_acc': val_acc,
                'test_loss': test_loss, 'test_acc': test_acc,'val_test_loss': val_test_loss, 'val_test_acc': val_test_acc}
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    torch.save(model.state_dict(), 'RoI_log/Res_Sim_RoI.pt') # Last model save

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val or test Acc: {:4f}'.format(best_acc))
    print('returning and looping back')

    return best_model

def exp_lr_scheduler(optimizer, epoch, init_lr = 0.001, lr_decay_epoch = 10):
    """Decay learning rate by a factor of DECAY_WEIGHT every lr_decay_epoch epochs."""
    lr = init_lr * (0.1**(epoch // lr_decay_epoch))

    if epoch % lr_decay_epoch == 0:
        print('LR is set to {}'.format(lr))

    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

    return optimizer


# Dataloader

train_df = pd.read_csv('train_df_box_roi.csv')
val_df = pd.read_csv('val_df_box_roi.csv')
test_df = pd.read_csv('test_df_box_roi.csv')

unique_imgs_train = train_df.ImageID.unique()
unique_imgs_val = val_df.ImageID.unique()
unique_imgs_test = test_df.ImageID.unique()

train_inds = list(range(len(unique_imgs_train)))
val_inds = list(range(len(unique_imgs_val)))
test_inds = list(range(len(unique_imgs_test)))

# 최대 num_workers = 8 in Colab.
train_dl = torch.utils.data.DataLoader(ResSimRoi(train_df, unique_imgs_train, train_inds, 'train'),
                                      batch_size = 64,
                                      shuffle = True,
                                      collate_fn = custom_collate,
                                      pin_memory= True if torch.cuda.is_available() else False,
                                      num_workers = 8,)

val_dl = torch.utils.data.DataLoader(ResSimRoi(val_df, unique_imgs_val, val_inds, 'val'),
                                      batch_size = 32,
                                      shuffle = True,
                                      collate_fn = custom_collate,
                                      pin_memory= True if torch.cuda.is_available() else False,
                                      num_workers = 8,)

test_dl = torch.utils.data.DataLoader(ResSimRoi(test_df, unique_imgs_test, test_inds, 'test'),
                                      batch_size = 32,
                                      shuffle = True,
                                      collate_fn = custom_collate,
                                      pin_memory= True if torch.cuda.is_available() else False,
                                      num_workers = 8,)

train_batch_num = (len(train_df) // 64) + 1
val_batch_num = (len(val_df) // 32) + 1
test_batch_num = (len(test_df) // 32)
val_test_batch_num = ((len(val_df) + len(test_df)) // 32) + 1

dset_loaders = {'train' : train_dl, 'val' : val_dl, 'test' : test_dl}
dset_sizes = {'train' : train_batch_num, 'val' : val_batch_num, 'test' : test_batch_num, 'val_test' : val_test_batch_num}

if __name__ == '__main__':

    # Train

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    model = SimRes50(mode = True)

    for layer in list(model.children())[:-3]:
        layer.train(mode = False)

        print('conv1.train   :', model.conv1.training)
        print('bn1.train     :', model.bn1.training)
        print('relu.train    :', model.relu.training)
        print('maxpool.train :', model.maxpool.training)
        print('layer1.train  :', model.layer1.training)
        print('layer2.train  :', model.layer2.training)
        print('layer3.train  :', model.layer3.training)
        print('layer4.train  :', model.layer4.training)
        print('avgpool.train :', model.avgpool.training)
        print('fc.train      :', model.fc.training)

    model.load_state_dict(torch.load('RoI_log/Res_Sim_RoI.pt')) # -> 이전에 학습한 Best 모델 load
    model.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer_ft = optim.SGD(model.parameters(), lr = 0.0001, momentum = 0.9, weight_decay = 0.0005)

    # Run the functions and save the best model in the function model_ft.
    model_ft = train_model(model, criterion, optimizer_ft, exp_lr_scheduler,
                        num_epochs = 30)

    # Save model
    torch.save(model_ft.state_dict(), 'RoI_log/fine_tuned_Res_Sim_RoI.pt')  # Learning completed model save

    # Evaluation
    model.eval()
    total = 0
    cnt = 0
    for data in test_dl:
        for _list in data:
            for tup in _list:
                inputs, labels = tup
                inputs = inputs.unsqueeze(0)
                inputs, labels = inputs.to(device), labels.to(device).long()
                output = model(inputs)

                _, preds = torch.max(output.data, 1)

                if labels ==  preds:
                    cnt += 1
                total += 1

    print(f'Test Accuracy: {cnt/total}')