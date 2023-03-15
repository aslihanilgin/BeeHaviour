class pred_val_extraction:
    x_mid = 0
    y_mid = 0
    # TODO: deltax, deltay, velocity

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

    def compute_velocity(self, db, current_img, prev_img):
        delta_t = video_frames[prev_img]['video_time'] - video_frames[current_img]['video_time']
        delta_y = compute_delta_y(db, prev_img)
        velocity = delta_y / delta_t
        
