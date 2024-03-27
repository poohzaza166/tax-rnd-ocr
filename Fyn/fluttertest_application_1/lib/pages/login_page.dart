import 'package:flutter/material.dart';
import 'package:fluttertest_application_1/components/my_texfield.dart';

class LogInPage extends StatelessWidget {
  LogInPage({super.key});

  //text editing control
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Color.fromARGB(250, 255, 255, 255),
        body: SafeArea(
          child: Center(
            child: Column(children: [
              const SizedBox(height: 300),
              Icon(
                Icons.account_circle_outlined,
                size: 100,
                color: Colors.grey[1000],
              ),
              const SizedBox(height: 50),
              Text(
                'Welcome back!',
                style: TextStyle(
                  fontSize: 24,
                  color: Colors.grey[1000],
                  fontFamily: 'San Francisco',
                ),
              ),
              const SizedBox(height: 20),
              MyTextField(
                controller: emailController,
                hintText: 'Email',
                obscureText: false,
              ),
              const SizedBox(height: 20),
              MyTextField(
                controller: passwordController,
                hintText: 'Password',
                obscureText: true,
              ),
              const SizedBox(height: 20),

              Text(
                'Forgot Password?',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[1000],
                  fontFamily: 'San Francisco',
                ),
              ),
              
              //LOGIN BUTTON
              const SizedBox(height: 10),

              Text(
                'New user? Create Account',
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[1000],
                  fontFamily: 'San Francisco',
                ),
              ),

            ]),
          ),
        ));
  }
}
