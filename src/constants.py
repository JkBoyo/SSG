from enum import Enum

Text_Type = Enum('Text_Type', ['text', 'bold', 'italic', 'code', 'link', 'image'])

Block_Type = Enum("Block_Type", ['paragraph', 'heading', 'code', 'quote', 'unordered_list', 'ordered_list'])