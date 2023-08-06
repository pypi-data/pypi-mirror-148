import math
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
class find_max_r2:
    """
    This class is used to find the best random state for the model
    x -> the independent variable
    y -> the dependent variable
    rgr -> the regressor"""
    def __init__(self) -> None:
        self.self=self
    def find_r2(rgr,x,y):
        global final_random_state,regressor,Highest_acc,MSE,MAE,RMSE
        final_random_state=[]#results will be append 
        regressor=[]#results will be append 
        Highest_acc=[]#results will be append 
        MSE=[]#results will be append 
        MAE=[]#results will be append 
        RMSE=[]#results will be append 
        def max_r2score(rgr,x,y):
            max_acc=0
            for rd in range(42,100):
                x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=rd,test_size=0.20)
                rgr.fit(x_train,y_train)
                prd=rgr.predict(x_test)
                acc=r2_score(y_test,prd)
                print("accuracy score for random state ",rd,"is ",acc)
                if acc>max_acc:
                    max_acc=acc
                    final_rd=rd
            mse=mean_squared_error(y_test,prd)#mean_squared_error
            mae=mean_absolute_error(y_test,prd)#mean_absolute_error
            rmse=math.sqrt(mse)#Root Mean Square Error
            print("max ccuracy score coresponding to ",final_rd,"♫is♫",max_acc*100)
            print("Mean_Squared_Error is: ",mse)
            print("Mean_Absolute_Error is: ",mae)
            print("Root Mean_Squared_Error is: ",rmse)
            final_random_state.append(final_rd)
            regressor.append(rgr)
            Highest_acc.append(max_acc*100)
            MSE.append(mse)
            MAE.append(mae)
            RMSE.append(rmse)
            return final_rd 
        max_r2score(rgr,x,y)
