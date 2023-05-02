class pred_val_extraction:
    x_mid = 0
    y_mid = 0

    def __init__(self, pred):
        self.pred = pred
        self.x_mid = self.extract_x_coord_mid(self.pred)
        self.y_mid = self.extract_y_coord_mid(self.pred)
        
    def extract_x_coord_mid(self, pred):
        return self.pred['predictions'][0]['x']

    def extract_y_coord_mid(self, pred):
        return self.pred['predictions'][0]['y']

    def compute_delta_x(self, db, current_img, prev_img):
        current_x =  self.x_mid
        prev_x = db[prev_img]['predictions'][0]['x']
        return prev_x - current_x

    def compute_delta_y(self, db, current_img, prev_img):
        current_y = self.y_mid
        prev_y = db[prev_img]['predictions'][0]['y']
        return prev_y - current_y

    def compute_velocity(y2, y1, t2, t1):
        delta_y = abs(y2 - y1)
        delta_t = abs(t2 - t1)
        if delta_t == 0:
            velocity = float("NaN")
        else:
            velocity = delta_y / delta_t
        return round(velocity,1)
        
