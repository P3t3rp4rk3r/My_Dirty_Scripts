from FacebookResetPasswordAPI import FacebookResetPasswordAPI
a = raw_input("email:")
res = FacebookResetPasswordAPI({'verbose': True}).get(a)
print res  # retrieves the results
