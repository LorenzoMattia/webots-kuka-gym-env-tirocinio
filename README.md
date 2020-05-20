# webots-kuka-gym-env-tirocinio
All'interno della cartella webots_kuka_gym_env_master/webots_controller/KukaReinLearn2 è presente sia il controllore da utilizzare su Webots (KukaReinLearn2.py), sia tutti i file con i dati dell'apprendimento fatto finora. 

Per ricominciare l'apprendimento da zero è necessario modficare la varibile continue_learning nel file learning_parameters impostandola a false.

Per avere dei riscontri più immediati avevamo inoltre settato il numero di epoche (variabile bbo_epochs in learning_parameters) per iterazione a 5, invece delle 50 di default.

Rispetto alla versione precedente è stato aggiornato anche il mondo con l'aggiunta di touch sensors sulle finger del robot. Il file del mondo è presente nella cartella webots_world.

Per l'installazione dell'ambiente gym e del mondo si può fare riferimento alla repository: https://github.com/gabrielesartor/webots-kuka-gym-env
