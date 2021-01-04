import React, { useState, useCallback, useEffect } from 'react'
import { GiftedChat } from 'react-native-gifted-chat'

import PubNub from 'pubnub';
import { PubNubProvider, usePubNub } from 'pubnub-react';

const pubnub = new PubNub({
  publishKey: 'pub-c-ad792232-e9fb-48b3-ad69-c63d62f95bc9',
  subscribeKey: 'sub-c-9245d3ec-4d41-11eb-a73a-1eec528e8f1f',
  uuid: 'myUniqueUUID'
});

function App() {
  return (<PubNubProvider client={pubnub}>
            <Chat />
          </PubNubProvider>);
}

function Chat() {
  const pubnub = usePubNub();
  const [messages, setMessages] = useState([]);
  const [channels] = useState(["ilabo"]);
  const handleMessage = event => {
    const message = event.message;
    if (typeof message === 'string' || message.hasOwnProperty('text')) {
      const text = message.text || message;
      addMessage(messages => [...messages, text]);
    }
  };
  useEffect(() => {
    pubnub.addListener({ message: handleMessage });
    pubnub.subscribe({ channels });

  }, [])

  const onSend = useCallback((messages = []) => {
    setMessages(previousMessages => GiftedChat.append(previousMessages, messages));
    console.log(messages);
    const mess = messages[0];
    pubnub.publish({channel: channels[0], mess}).then(() => setMessage(""));
  }, [])

  return (
    <GiftedChat
      messages={messages}
      onSend={messages => onSend(messages)}
      user={{
        _id: 1,
      }}
    />
  )
}

export default App;