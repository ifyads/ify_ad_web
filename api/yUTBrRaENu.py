from flask import Flask, render_template , redirect, url_for

import bcrypt


def hash_password(password ,salt):

  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  
  return (hashed_password)



def r3KGwEgXI1(user, password ):

 salt= b'$2b$12$RVqVqHmhWNnWCXn4ntKjCe'
 

 entered= hash_password(password , salt)

 if entered == b'$2b$12$RVqVqHmhWNnWCXn4ntKjCeVYAjdHHA8RkFlPxJYT3FuHC4OfSbWPS':
  if user == "ADMIN":
    return render_template("/admin/log625/7x0ah1JM6n.html")
  else:
    return redirect(url_for("linkshortener"))
 else:
  return redirect(url_for("linkshortener"))

 



       
