from django.db import models
from slack_cache import settings
# Create your models here.
import slack


class ChannelManager(models.Manager):
    def __parse_fields(self,channel_list):
        """
        this is a function that extract the required fields from a dict object 

        Args:
            channel_list (:obj:`list` of :obj:`dict`): is the list of channels with all fields
        Returns:
            :obj:`list` of :obj:`dict` : a list of objects with the fields specified in the model.
        """
        fields = [field.name for field in self.model._meta.get_fields()]
        PARSED_CHANNEL_LIST = []
        for ch in channel_list["channels"]:
            PARSED_CHANNEL_LIST.append({
                field: ch[field] if field!='id' else ch['slack_id'] for field in fields
            })
        
        return PARSED_CHANNEL_LIST
    def __parse_fields_th(self,message_list):
        """
        this is a function that extract the required fields from a dict object 

        Args:
            message_list (:obj:`list` of :obj:`dict`): is the list of messages with all fields
        Returns:
            :obj:`list` of :obj:`dict` : a list of objects with the fields specified in the model.
        """
        fields = [field.name for field in Thread._meta.get_fields()]
        PARSED_CHANNEL_LIST = []
        for ch in message_list["messages"]:
            PARSED_CHANNEL_LIST.append({
                field: ch[field] if field!="channel" else "" for field in fields
            })
        return PARSED_CHANNEL_LIST
    def update_slack_channels(self):
        client = slack.WebClient(token=self.model._meta.token)
        channel_list = client.channels_list()
        if channel_list["ok"]:
            fields_parsed = self.__parse_fields(channel_list())
            for ch in fields_parsed:
                try:
                    ch_obj = self.model(**ch)
                    ch_obj.save()
                except Exception as e:
                    print(e)
    def update_channel_threads(self):
        all_obj = self.get_queryset().all()
        for obj in all_obj :
            s_id = obj.slack_id
            client = slack.WebClient(token=self.model._meta.token)
            history = client.channels_history(channel=s_id)
            parsed = self.__parse_fields_th(history)
            for th in parsed:
                th.pop('channel')
                nth=Thread(**th,channel=obj)
                nth.save()
        # do someth
class Channel(models.Model):
    """Model definition for Channel."""
    slack_id  = models.CharField(max_length=100, unique=True)
    name=models.CharField(max_length=100, unique=True)
    is_private = models.BooleanField(default=False)
    num_members = models.IntegerField()
    is_archived = models.BooleanField(default=False)
    objects = models.Manager()
    populate = ChannelManager()
    # TODO: Define fields here

    class Meta:
        """Meta definition for Channel."""

        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'
        token = settings.SLACK_API_TOKEN

    def __str__(self):
        """Unicode representation of Channel."""
        pass



    

# this is a base class for threads , it'll be inherited to work with files and messages
class Thread(models.Model):
    """Model definition for Thread."""
    ts = models.CharField(max_length=140)
    user = models.CharField(max_length=140)
    channel  = models.ForeignKey('message_app.Channel', related_name='channel', on_delete=models.CASCADE) 

    # TODO: Define fields here

    class Meta:
        """Meta definition for Thread."""

        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        token = settings.SLACK_API_TOKEN

    def __str__(self):
        """Unicode representation of Thread."""
        pass

# todo replies