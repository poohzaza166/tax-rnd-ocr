import 'package:flutter/material.dart';

class MyTextField extends StatelessWidget {
  final controller;
  final String? hintText;
  final bool obscureText;
  final Widget? suffixIcon;

  const MyTextField({
    Key? key,
    required this.controller,
    this.hintText,
    this.obscureText = false,
    this.suffixIcon,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25.0),
      child: TextField(
        controller: controller,
        obscureText: obscureText,
        decoration: InputDecoration(
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Color.fromARGB(255, 255, 255, 255)),
            borderRadius: BorderRadius.circular(20),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Color.fromARGB(255, 255, 255, 255)),
            borderRadius: BorderRadius.circular(20),
          ),
          fillColor: Color.fromARGB(255, 243, 243, 245),
          filled: true,
          hintText: hintText,
          suffixIcon: suffixIcon,
          hintStyle: const TextStyle(
            color: Color.fromRGBO(64, 100, 250, 0.6),
          ),
        ),
      ),
    );
  }
}
