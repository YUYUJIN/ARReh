// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'RehItem.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

RehList _$RehListFromJson(Map<String, dynamic> json) => RehList(
      list: (json['list'] as List<dynamic>?)
          ?.map((e) => RehItem.fromJson(e as Map<String, dynamic>))
          .toList(),
    );

Map<String, dynamic> _$RehListToJson(RehList instance) => <String, dynamic>{
      'list': instance.list,
    };

RehItem _$RehItemFromJson(Map<String, dynamic> json) => RehItem(
      part: json['part'] as String,
      image: json['image'] as String,
      name: json['name'] as String,
      time: json['time'] as int,
    );

Map<String, dynamic> _$RehItemToJson(RehItem instance) => <String, dynamic>{
      'part': instance.part,
      'image': instance.image,
      'name': instance.name,
      'time': instance.time,
    };
