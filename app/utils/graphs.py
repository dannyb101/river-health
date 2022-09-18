import plotly.express as px
import plotly
# import os
# os.environ["PATH"] = os.environ["PATH"] + ";...venv3.9\\lib\\site-packages\\kaleido\\executable\\"
from app.Connections.fs_server import FS_SERVER

class Graph:

    #Created graph object
    def __init__(self, df, post_ninetynine_percentile, pre_ninetynine_percentile, title, isBOD):
        self.df = df
        self.post_ninetynine_percentile = post_ninetynine_percentile
        self.pre_ninetynine_percentile = pre_ninetynine_percentile
        self.title = title
        self.isBOD = isBOD

    def create_and_save_graph_99(self, *, unique_id: str):
        if self.isBOD:
            #created histogram using passed concentrations from dataframe column
            fig = px.histogram(x=self.df['mix_bod_mg/l'], nbins=300, labels=dict(x="BOD concentration (mg/l)"))
            #adds the vertical line at the level on the x axis where the post-spill 99th percentile falls
            fig.add_vline(x=self.post_ninetynine_percentile, line_width=3,line_color="red", annotation_text="Post spill 99th percentile = "+str(self.post_ninetynine_percentile)+" mg/l", annotation_position="top right", annotation_font_color="red", annotation_textangle = 90)
            #adds the vertical line at the level on the x axis where the pre-spill 99th percentile falls
            fig.add_vline(x=self.pre_ninetynine_percentile, line_width=3,line_color="orange", annotation_text="Pre spill 99th percentile = "+str(self.pre_ninetynine_percentile)+" mg/l", annotation_position="top", annotation_font_color="orange")
            #calculates the end of the x axis so that the majority of the values are shown more prominently
            end_graph_bod = (self.post_ninetynine_percentile*1.25)
            #range of x axis
            fig.update_xaxes(range=[0, end_graph_bod])
            #creates html card to be inserted into outputs.html
        else:
            fig = px.histogram(x=self.df['mix_nh3_mg/l'], nbins=500, labels=dict(x="Ammonia concentration (mg/l)"))
            fig.add_vline(x=self.post_ninetynine_percentile, line_width=3,line_color="red",  annotation_text="Post spill 99th percentile = "+str(self.post_ninetynine_percentile)+" mg/l", annotation_position="top right", annotation_font_color="red", annotation_textangle = 90)
            fig.add_vline(x=self.pre_ninetynine_percentile, line_width=3,line_color="orange", annotation_text="Pre spill 99th percentile = "+str(self.pre_ninetynine_percentile)+" mg/l", annotation_position="top", annotation_font_color="orange")
            end_graph_nh3 = (self.post_ninetynine_percentile*1.25)
            fig.update_xaxes(range=[0, end_graph_nh3])
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)


        file_server_connection = FS_SERVER()
        if self.isBOD:
            fig.write_html("./app/Local_File_Storage/BOD_GRAPH/" + unique_id)
            file_server_connection.save_local_file_to_remote(folder_name='BOD_GRAPH', unique_id=unique_id)
        else:
            fig.write_html("./app/Local_File_Storage/NH3_GRAPH/" + unique_id)
            file_server_connection.save_local_file_to_remote(folder_name='NH3_GRAPH', unique_id=unique_id)