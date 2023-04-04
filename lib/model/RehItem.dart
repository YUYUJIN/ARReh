import 'package:json_annotation/json_annotation.dart';

part 'RehItem.g.dart';

@JsonSerializable()
class RehList {
  List<RehItem>? list;

  RehList({
    required this.list,
  });

  factory RehList.fromJson(Map<String, dynamic> json) =>
      _$RehListFromJson(json);

  Map<String, dynamic> toJson() => _$RehListToJson(this);
}

@JsonSerializable()
class RehItem {
  String part;
  String image;
  String name;
  int time;

  RehItem({
    required this.part,
    required this.image,
    required this.name,
    required this.time,
  });

  factory RehItem.fromJson(Map<String, dynamic> json) =>
      _$RehItemFromJson(json);

  Map<String, dynamic> toJson() => _$RehItemToJson(this);
}