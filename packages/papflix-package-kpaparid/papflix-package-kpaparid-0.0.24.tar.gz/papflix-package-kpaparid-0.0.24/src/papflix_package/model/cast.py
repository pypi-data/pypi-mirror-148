class Cast():
    cast_id =0
    character = ''
    credit_id = 0
    gender = 0
    id = 0
    name =''
    order = 0
    profile_path = ''


    def __init__(self, cast):
        self.cast_id = cast['cast_id']
        self.character = cast['character']
        self.credit_id = cast['credit_id']
        self.gender = cast['gender']
        self.id = cast['id']
        self.name = cast['name']
        self.order = cast['order']



        # print(cast['profile_path'])
        if(cast['profile_path'] == None) :
            self.profile_path = 'null'
        else:
            self.profile_path = cast['profile_path']
        # print(self.profile_path)


